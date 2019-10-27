//
//  CreateAccountViewController.swift
//  Now
//
//  Created by Ivan Grachev on 26.10.2019.
//  Copyright © 2019 Ivan Grachev. All rights reserved.
//

import UIKit

struct Place {
    let name: String
    var isSelected: Bool
}

class CreateAccountViewController: UIViewController {

    var places = firstBatch
    
    @IBOutlet weak var tableView: UITableView! {
        didSet {
            tableView.delegate = self
            tableView.dataSource = self
        }
    }
    
    @IBOutlet weak var okButton: UIButton!
    
    private var isSecondBatch = false
    
    @IBAction func okButtonTapped(_ sender: Any) {
        if isSecondBatch {
            DefaultsService.shared.didFinishConfiguration = true
            let search = instantiate(SearchViewController.self)
            search.modalPresentationStyle = .fullScreen
            search.modalTransitionStyle = .crossDissolve
            present(search, animated: true)
        } else {
            isSecondBatch = true
            places = secondBatch
            tableView.reloadData()
            okButton.setTitle("OK", for: .normal)
        }
    }
}

extension CreateAccountViewController: UITableViewDelegate {
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        places[indexPath.row].isSelected.toggle()
        let isSelected = places[indexPath.row].isSelected
        tableView.cellForRow(at: indexPath)?.accessoryType = isSelected ? .checkmark : .none
    }
}

extension CreateAccountViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return places.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "place", for: indexPath)
        let place = places[indexPath.row]
        cell.textLabel?.text = place.name
        cell.accessoryType = place.isSelected ? .checkmark : .none
        return cell
    }
}


let firstBatch = ["Fish & Meat", "Bratya Karavaevy", "MacDonalds", "Bright Israel Grill", "M!cRobe", "Pushkin", "Starlite Diner", "Progress Bar", "Sowl in the bowl", "Nude", "BB Burgers", "Burger Heros", "Zotman Pizza Pie"].map { Place(name: $0, isSelected: false) }
let secondBatch = ["United Asia", "Murakame", "Starbucks", "Shokoladnitza", "Coffemania", "Khinkali Point", "Brusnika", "Chayhona", "Blush", "Dom Kultur", "Varenichnaya №1", "I love cake", "Remy bar and kitchen"].map { Place(name: $0, isSelected: false) }
