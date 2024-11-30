//
//  URL+whyFinanceBaseURL.swift
//  WhyFinanceApp
//
//  Created by Alessio Giordano on 28/11/24.
//

import Foundation

extension URL {
    static var whyFinanceGithubCodespacesURL: URL { .init(string: "https://fictional-disco-vqq7jv4wpv736x45-80.app.github.dev/")! }
    static var whyFinanceBaseURL: URL { .init(string: "http://localhost:80/")! }
    
    static func whyFinanceBaseURL(host: String?) -> URL? {
        let baseURL: URL
        if let host, !host.isEmpty {
            if host.hasPrefix("http://") || host.hasPrefix("https://") {
                if let url = URL(string: host) {
                    baseURL = url
                } else {
                    return nil
                }
            } else {
                if let url = URL(string: "http://" + host) {
                    baseURL = url
                } else {
                    return nil
                }
            }
        } else {
            baseURL = .whyFinanceBaseURL
        }
        return baseURL
    }
}
