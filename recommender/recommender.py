import pandas as pd
import numpy as np
import annoy
import surprise


class Index:
    def __init__(self, dimension):
        self.index = annoy.AnnoyIndex(dimension, 'dot')

    def build(self, vectors, n_trees=10):
        for i, vector in enumerate(vectors):
            self.index.add_item(i, vector)
        self.index.build(n_trees)

    def search(self, profile, n_closest=20):
        return self.index.get_nns_by_vector(profile, n_closest, include_distances=True)


class Vocab:
    def __init__(self):
        self.ids = []
        self.id_to_index = {}

    def add_ids(self, ids):
        for id in ids:
            if id not in self.id_to_index:
                self.id_to_index[id] = len(self.id_to_index)
                self.ids.append(id)

    def ids_to_indices(self, ids):
        ids = np.array([self.id_to_index.get(id, -1) for id in ids])
        return ids, ids == -1

    def indices_to_ids(self, indices):
        return [self.ids[index] for index in indices]


class PMF:
    def __init__(self, dimensions=20, rating_scale=(1, 5)):
        self.dimensions = dimensions
        self.rating_scale = rating_scale
        self.svd = surprise.SVD(dimensions, biased=False, random_state=42)
        self.user_vocab = Vocab()
        self.item_vocab = Vocab()

    def fit(self, user_ids, item_ids, ratings):
        self.user_vocab.add_ids(user_ids)
        self.item_vocab.add_ids(item_ids)
        user_indices, _ = self.user_vocab.ids_to_indices(user_ids)
        item_indices, _ = self.item_vocab.ids_to_indices(item_ids)
        dataset = surprise.Dataset.load_from_df(
            pd.DataFrame(dict(user_id=user_indices, item_id=item_indices, rating=ratings)),
            reader=surprise.Reader(rating_scale=self.rating_scale))
        trainset = dataset.construct_trainset(dataset.raw_ratings)
        self.svd.fit(trainset)
        self.user_profiles = self.svd.pu
        self.item_profiles = self.svd.qi
        self.global_mean = trainset.global_mean

    def predict(self, user_ids, item_ids):
        user_indices, user_unknown = self.user_vocab.ids_to_indices(user_ids)
        item_indices, item_unknown = self.item_vocab.ids_to_indices(item_ids)
        unknown = user_unknown | item_unknown
        ratings = (self.user_profiles[user_indices] * self.item_profiles[item_indices]).sum(axis=1)
        ratings[unknown] = 0
        return ratings + self.global_mean

    def build_index(self):
        self.index = Index(self.dimensions)
        self.index.build(self.item_profiles)

    def search(self, user_id=None, item_id=None, n_closest=20):
        assert (user_id is not None) != (item_id is not None)
        if user_id is not None:
            profile = self.user_profiles[self.user_vocab.id_to_index[user_id]]
        if item_id is not None:
            profile = self.item_profiles[self.item_vocab.id_to_index[item_id]]
        indices, distances = self.index.search(profile, n_closest)
        return self.item_vocab.indices_to_ids(indices), distances


class Recommender:
    def __init__(self, df):
        self.df = df

    def recommend(self, item_ids, ratings, n_closest=20, binary_rating=False):
        new_df = self.df.copy()
        for item_id, rating in zip(item_ids, ratings):
            new_df.loc[len(new_df)] = [item_id, 'new_user', rating, '', '', '']
        model = PMF(rating_scale=(0, 1) if binary_rating else (1, 5))
        rating = new_df.rating
        if binary_rating:
            rating = (rating >= 4).astype(int)
        model.fit(new_df.user_id, new_df.org_id, rating)
        model.build_index()
        return model.search(user_id='new_user', n_closest=n_closest)


recommender = Recommender(pd.read_csv('orgs_merged.csv'))
recommender.recommend(
    ['ChIJzX3TaKRLtUYRWXxaqlv-Mec', 'ChIJz4hlXAVLtUYRnQx4_-WcWTk', 'ChIJv6ZyGJ9LtUYRvKjPR427PjY'],
    [5, 5, 5],
    binary_rating=False)[0]