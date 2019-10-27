//
//  FeedbackViewController.swift
//  Now
//
//  Created by Ivan Grachev on 26.10.2019.
//  Copyright © 2019 Ivan Grachev. All rights reserved.
//

import UIKit

class FeedbackViewController: UIViewController {
    
    @IBOutlet weak var nameLabel: UILabel!
    
    @IBOutlet weak var mehButton: SelectableButton!
    @IBOutlet weak var neutralButton: SelectableButton!
    @IBOutlet weak var loveButton: SelectableButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        if let name = DefaultsService.shared.placeName {
            nameLabel.text = name + "?"
        }
        DefaultsService.shared.placeName = nil
    }
    
    @IBAction func mehButtonTapped(_ sender: Any) {
        if loveButton.addedBackground {
            loveButton.switchBackground()
        }
        if neutralButton.addedBackground {
            neutralButton.switchBackground()
        }
        mehButton.switchBackground()
    }
    
    @IBAction func neutralButtonTapped(_ sender: Any) {
        if loveButton.addedBackground {
            loveButton.switchBackground()
        }
        if mehButton.addedBackground {
            mehButton.switchBackground()
        }
        neutralButton.switchBackground()
    }
    
    @IBAction func loveButtonTapped(_ sender: Any) {
        if neutralButton.addedBackground {
            neutralButton.switchBackground()
        }
        if mehButton.addedBackground {
            mehButton.switchBackground()
        }
        loveButton.switchBackground()
    }
    
    @IBAction func doneButtonTapped(_ sender: Any) {
        let search = instantiate(SearchViewController.self)
        search.modalPresentationStyle = .fullScreen
        search.modalTransitionStyle = .crossDissolve
        present(search, animated: true)
    }
}
