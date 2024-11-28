//
//  WhyFinanceApp.swift
//  WhyFinanceApp
//
//  Created by Alessio Giordano on 28/11/24.
//

import SwiftUI

struct VerticalPositionReader: View {
    @Binding var position: CGFloat
    let coordinateSpace: CoordinateSpace
    
    var body: some View {
        GeometryReader { proxy in
            Color.clear
                .frame(height: 0)
                .frame(maxWidth: .infinity)
                .onChange(of: proxy.frame(in: coordinateSpace), initial: true) { _, frame in
                    position = -1 * frame.minY
                }
        }.frame(height: 0)
    }
}
