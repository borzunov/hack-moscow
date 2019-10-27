//
//  SearchViewController.swift
//  Now
//
//  Created by Ivan Grachev on 26.10.2019.
//  Copyright © 2019 Ivan Grachev. All rights reserved.
//

import UIKit

class SearchViewController: UIViewController {

    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!
    @IBOutlet weak var goButton: UIButton!
    
    var cityCentter = false
    
    @IBAction func goButtonTapped(_ sender: Any) {
        goButton.isHidden = true
        activityIndicator.startAnimating()
        activityIndicator.isHidden = false
        
        getRecommendation(cityCenter: cityCentter) { [weak self] recommendation in
            let recommendation = recommendation ?? Recommendation(name: "Khinkali Point", lat: 55.780921, lng: 37.592727, travel_time_mins: 21, photo_url: nil)
            let recommendationVC = instantiate(RecommendationViewController.self)
            recommendationVC.modalPresentationStyle = .fullScreen
            recommendationVC.modalTransitionStyle = .crossDissolve
            recommendationVC.recommendation = recommendation
            self?.present(recommendationVC, animated: true)
        }
    }
    
    @IBAction func featuredButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func wifiButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func newButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func familyButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func atmosphericButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func takeawayButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func fastButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func closeButtonTapped(_ sender: SelectableButton) {
        cityCentter.toggle()
        sender.switchBackground()
    }
    
    @IBAction func cheapButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func dateButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func musicButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func classyButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func coffeButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func drinnksButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func breakfstButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func lunchButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func dessertsButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func fishButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func meatButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func saladsButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func pizzaButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func burgersButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func sushiButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func iceButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func tropicalButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func pastaButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    
    
    @IBAction func healthyButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    @IBAction func veganButtonTapped(_ sender: SelectableButton) {
        sender.switchBackground()
    }
    
    
    
}
