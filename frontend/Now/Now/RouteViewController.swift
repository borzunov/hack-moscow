//
//  RouteViewController.swift
//  Now
//
//  Created by Ivan Grachev on 26.10.2019.
//  Copyright © 2019 Ivan Grachev. All rights reserved.
//

import UIKit
import NMAKit

class RouteViewController: UIViewController {

    var recommendation: Recommendation!
    
    @IBOutlet weak var mapView: NMAMapView!
    @IBOutlet weak var nameLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        nameLabel.text = recommendation.name
        DefaultsService.shared.placeName = recommendation.name
    }
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        let otherPoint = NMAGeoCoordinates(latitude: 55.815494, longitude: 37.575396)
        let center = NMAGeoCoordinates(latitude: recommendation.lat, longitude: recommendation.lng)
        mapView.set(geoCenter: center, animation: NMAMapAnimation.none)
        mapView.copyrightLogoPosition = NMALayoutPosition.bottomRight
        mapView.zoomLevel = 14
        mapView.backgroundColor = UIColor.systemBackground
        let startmarker = NMAMapMarker(geoCoordinates: otherPoint, image: UIImage(named: "redpin")!)
        let marker = NMAMapMarker(geoCoordinates: center, image: UIImage(named: "pin")!)
        mapView.add(mapObject: startmarker)
        mapView.add(mapObject: marker)
        let routingMode = NMARoutingMode(routingType: .fastest, transportMode: .car, routingOptions: .init())
        router.calculateRoute(withPoints: [otherPoint, center], routingMode: routingMode) { [weak self] (result, erro) in
            guard let route = result?.routes?.first, let mapRoute = NMAMapRoute.init(route) else { return }
            self?.mapView.add(mapObject: mapRoute)
        }
    }
    
    private let router = NMACoreRouter()
    
    @IBAction func feedbackButtonTapped(_ sender: Any) {
        let feedback = instantiate(FeedbackViewController.self)
        feedback.modalPresentationStyle = .fullScreen
        feedback.modalTransitionStyle = .crossDissolve
        present(feedback, animated: true)
    }
}
