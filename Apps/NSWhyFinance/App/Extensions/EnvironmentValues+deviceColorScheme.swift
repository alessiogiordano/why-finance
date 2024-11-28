//
//  EnvironmentValues+whyFinanceBaseURL.swift
//  WhyFinanceApp
//
//  Created by Alessio Giordano on 28/11/24.
//

import SwiftUI

struct WhyFinanceBaseURLKey: EnvironmentKey {
    static let defaultValue = URL.whyFinanceBaseURL
}

extension EnvironmentValues {
    var whyFinanceBaseURL: URL {
        get { self[WhyFinanceBaseURLKey.self] }
        set { self[WhyFinanceBaseURLKey.self] = newValue }
    }
}
