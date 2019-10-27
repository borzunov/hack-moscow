//
//  RecommendationViewController.swift
//  Now
//
//  Created by Ivan Grachev on 26.10.2019.
//  Copyright © 2019 Ivan Grachev. All rights reserved.
//

import UIKit
import Kingfisher

class RecommendationViewController: UIViewController {
    
    var recommendation: Recommendation!
    
    @IBOutlet weak var routeButton: UIButton! {
        didSet {
            routeButton.layer.cornerRadius = 27
        }
    }
    
    @IBOutlet weak var friendLabel: UILabel!
    @IBOutlet weak var photoImageView: UIImageView!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var reasonLabel: UILabel!
    @IBOutlet weak var distanceLabel: UILabel!
    
    var reasons = ["Because you enjoyed Blush", "Something different", "Because you like good coffee", "Your friends like it", "The best food in the city", "Featured on the Village", "Iconic place"]
    var friends = ["Vadim Zakharenko", "Indar Maremukhov", "Olga Soboleva", "Alexey Ustimenko", "Stepan Perminov", "Masha Petrova", "Dima Yakovlev", "Asya Twain"]
    var howLongAgo = ["a day ago", "2 hours ago", "just now", "a week ago", "3 weeks ago", "5 days ago", "2 weeks ago"]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        reasonLabel.text = reasons[Int.random(in: 0..<reasons.count)]
        friendLabel.text = friends[Int.random(in: 0..<friends.count)] + " was there " + howLongAgo[Int.random(in: 0..<howLongAgo.count)]
        
        nameLabel.text = recommendation.name
        distanceLabel.text = "\(Int(recommendation.travel_time_mins)) minutes away"
        if let urlString = recommendation.photo_url, let url = URL(string: urlString) {
            photoImageView.kf.setImage(with: url)
        } else {
            photoImageView.image = UIImage(named: "photo")
        }
    }
    
    @IBAction func showRouteButtonTapped(_ sender: Any) {
        let route = instantiate(RouteViewController.self)
        route.recommendation = recommendation
        route.modalPresentationStyle = .fullScreen
        route.modalTransitionStyle = .crossDissolve
        present(route, animated: true)
    }
}
