//
//  AppDelegate.swift
//  Now
//
//  Created by Ivan Grachev on 26.10.2019.
//  Copyright © 2019 Ivan Grachev. All rights reserved.
//

import UIKit
import NMAKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool { 
        NMAApplicationContext.setAppId("iUfkwrWhwDWcw2Ta5F5N", appCode: "Q-UnkCdx3ll8UAs8fhG4PQ", licenseKey: "fe+8W6/0NWdnVycdxZfXBEe5tHooO2u8qz35x+Q4/gXZJSqYEYzER3jQGpCDdu8oYkEtkLiozRi2dxvonNJXm1Ubtx1TqlIfvNBPLGQMcmu0BGHAh8n2f/AtTvOfAZCyPH85aNsalsVrFkqm8bEsPkA+qQkDg0nCT2sbHCVhoymitM1T50LGZd0RqW1Mr2kLvWeS8i1LF3OP7tA64iwRkyO2OqalvJWGKpk3q8FIG7pfGZvW4PHEMJJOHCWVYaeMs2WOphqfVhMP0NCPygBaOoaM5rzEeIF6eP1lnLzcdxt2W14v2C1EljL5w1cq49DOcTX9jtkrYCog8YuUHq5Gsx0MPCGgVMjA7n6yE7Bs0+A/2goFPkhm+VXybIE4Mg2z1do29+kT0+8ub9NC8h/ra8WbwNiigGjGR1esTw2owAv53dZjrG/b26mEpDbW1AFFSCKY1d53ivgTK4Y2v2tFLMssxR3JJTYaC6sxq01AWAGlP4NAzmHVcmR/dCDRdocMUUtg9ii6Ch3ikGowVwE9qosimnruF0fHJqJk9HD+6MnU1KlVmaBc6CCoXMPqWd7BKQFegK7PgI2acKJbV0jqhp9/2AcMVaG9mqBSCM5OUxDYd4Zw7sFQWQnwyEFrwvCPhz/t09tNIHC5Gb/WEEj6dFODGt0hPLD2JsGO7T2+RHQ=")
        return true
    }

    // MARK: UISceneSession Lifecycle

    func application(_ application: UIApplication, configurationForConnecting connectingSceneSession: UISceneSession, options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        // Called when a new scene session is being created.
        // Use this method to select a configuration to create the new scene with.
        return UISceneConfiguration(name: "Default Configuration", sessionRole: connectingSceneSession.role)
    }

    func application(_ application: UIApplication, didDiscardSceneSessions sceneSessions: Set<UISceneSession>) {
        // Called when the user discards a scene session.
        // If any sessions were discarded while the application was not running, this will be called shortly after application:didFinishLaunchingWithOptions.
        // Use this method to release any resources that were specific to the discarded scenes, as they will not return.
    }


}

