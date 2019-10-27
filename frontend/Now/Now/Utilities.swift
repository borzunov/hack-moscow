//
//  Utilities.swift
//  Now
//
//  Created by Ivan Grachev on 26.10.2019.
//  Copyright © 2019 Ivan Grachev. All rights reserved.
//

import UIKit

func instantiate<ViewControllerType>(_ type: ViewControllerType.Type) -> ViewControllerType {
    return UIStoryboard(name: "Main", bundle: nil).instantiateViewController(withIdentifier: String(describing: type)) as! ViewControllerType
}

extension UIColor {
    static var main: UIColor {
        return UIColor(red: 166 / 255, green: 71 / 255, blue: 218 / 255, alpha: 1)
    }
}

class DefaultsService {
    
    static let shared = DefaultsService()
    private let userDefaults = UserDefaults.standard
    
    var placeName: String? {
        get {
            return userDefaults.string(forKey: #function)
        }
        set {
            userDefaults.set(newValue, forKey: #function)
        }
    }
    
    var didFinishConfiguration: Bool {
        get {
            return userDefaults.bool(forKey: #function)
        }
        set {
            userDefaults.set(newValue, forKey: #function)
        }
    }
}

class SelectableButton: UIButton {
    
    var addedBackground = false
    
    var didSetup = false
    
    func switchBackground() {
        if !didSetup {
            didSetup = true
            layer.cornerRadius = 5
        }
        
        addedBackground = !addedBackground
        if addedBackground {
            backgroundColor = UIColor.main.withAlphaComponent(0.7)
            tintColor = UIColor.white
        } else {
            backgroundColor = UIColor.clear
            tintColor = UIColor.link
        }
    }
    
}

struct RecommendationRequest: Codable {
    let user_id: String
    let lat: Double
    let lng: Double
}

struct Recommendation: Codable {
    let name: String
    let lat: Double
    let lng: Double
    let travel_time_mins: Double
    let photo_url: String?
}

func getRecommendation(cityCenter: Bool, completion: @escaping ((Recommendation?) -> Void)) {
    let lat = cityCenter ? "55.778295" : "55.815494"
    let lng = cityCenter ? "37.594294" : "37.575396"
    let url = URL(string: "http://84.201.151.219:5000/api/recommend?user_id=5f29f9df-6c85-4dfe-822c-83b450bc043d&lat=\(lat)&lng=\(lng)")!
    let dataTask = URLSession.shared.dataTask(with: url) { data, response, error in
        DispatchQueue.main.async {
            guard let data = data else {
                completion(nil)
                return
            }
            let decoder = JSONDecoder()
            completion(try? decoder.decode(Recommendation.self, from: data))
        }
    }
    dataTask.resume()
}
