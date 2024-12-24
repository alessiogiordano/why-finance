//
//  StringCodable.swift
//  NSWhyFinance
//
//  Created by Alessio Giordano on 23/12/24.
//

import Foundation
import SwiftUI

public protocol StringCodable: Codable {}

extension Optional: @retroactive RawRepresentable where Wrapped: StringCodable {
    public typealias RawValue = String?
    
    public init?(rawValue: String?) {
        guard let rawData = rawValue?.data(using: .utf8),
              let user = try? JSONDecoder().decode(Wrapped.self, from: rawData)
        else { return nil }
        self = user
    }
    public var rawValue: String? {
        guard let rawData = (try? JSONEncoder().encode(self)),
              let rawValue = String(data: rawData, encoding: .utf8)
        else { return nil }
        return rawValue
    }
}
