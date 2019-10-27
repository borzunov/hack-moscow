//
//  WelcomeViewController.swift
//  Now
//
//  Created by Ivan Grachev on 26.10.2019.
//  Copyright © 2019 Ivan Grachev. All rights reserved.
//

import UIKit

class WelcomeViewController: UIViewController {
    
    @IBAction func okButtonTapped(_ sender: Any) {
        let createAccount = instantiate(CreateAccountViewController.self)
        createAccount.modalPresentationStyle = .fullScreen
        createAccount.modalTransitionStyle = .crossDissolve
        present(createAccount, animated: true)
    }
}
