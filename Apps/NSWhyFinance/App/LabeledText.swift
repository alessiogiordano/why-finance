//
//  LabeledText.swift
//  WhyFinanceApp
//
//  Created by Alessio Giordano on 28/11/24.
//

import SwiftUI

struct LabeledText: View {
    let label: String
    let value: String
    var body: some View {
        #if os(macOS)
        LabeledContent(label) {
            Text(value).foregroundStyle(.secondary)
        }
        #else
        HStack {
            Text(label)
            Spacer()
            Text(value).foregroundStyle(.secondary)
        }
        #endif
    }
}
