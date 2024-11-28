//
//  VisualEffectBackground.swift
//  Tombola (macOS)
//
//  Created by Alessio Giordano on 15/08/20.
//

#if os(macOS)

import SwiftUI
import AppKit
import Cocoa

/**********************/

struct visualEffectMaterialKey: EnvironmentKey {
    static var defaultValue: NSVisualEffectView.Material? = nil
}

extension EnvironmentValues {
    var visualEffectMaterial: NSVisualEffectView.Material? {
        get { self[visualEffectMaterialKey.self] }
        set { self[visualEffectMaterialKey.self] = newValue }
    }
}

/**********************/

struct visualEffectBlendingKey: EnvironmentKey {
    static var defaultValue: NSVisualEffectView.BlendingMode? = nil
}

extension EnvironmentValues {
    var visualEffectBlending: NSVisualEffectView.BlendingMode? {
        get { self[visualEffectBlendingKey.self] }
        set { self[visualEffectBlendingKey.self] = newValue }
    }
}

/**********************/

struct visualEffectEmphasizedKey: EnvironmentKey {
    static var defaultValue: Bool? = nil
}

extension EnvironmentValues {
    var visualEffectEmphasized: Bool? {
        get { self[visualEffectEmphasizedKey.self] }
        set { self[visualEffectEmphasizedKey.self] = newValue }
    }
}

/**********************/

struct VisualEffectBackground: NSViewRepresentable {
    private let material: NSVisualEffectView.Material
    private let blendingMode: NSVisualEffectView.BlendingMode
    private let isEmphasized: Bool
    
    fileprivate init(
        material: NSVisualEffectView.Material,
        blendingMode: NSVisualEffectView.BlendingMode,
        emphasized: Bool) {
        self.material = material
        self.blendingMode = blendingMode
        self.isEmphasized = emphasized
    }
    
    func makeNSView(context: Context) -> NSVisualEffectView {
        let view = NSVisualEffectView()
        
        // Not certain how necessary this is
        view.autoresizingMask = [.width, .height]
        
        return view
    }
    
    func updateNSView(_ nsView: NSVisualEffectView, context: Context) {
        nsView.material = context.environment.visualEffectMaterial ?? material
        nsView.blendingMode = context.environment.visualEffectBlending ?? blendingMode
        nsView.isEmphasized = context.environment.visualEffectEmphasized ?? isEmphasized
    }
}

extension View {
    func visualEffect(
        material: NSVisualEffectView.Material,
        blendingMode: NSVisualEffectView.BlendingMode = .behindWindow,
        emphasized: Bool = false,
        ignoresSafeArea regions: SafeAreaRegions? = nil
    ) -> some View {
        background {
            if let regions {
                VisualEffectBackground(
                    material: material,
                    blendingMode: blendingMode,
                    emphasized: emphasized
                ).ignoresSafeArea(regions)
            } else {
                VisualEffectBackground(
                    material: material,
                    blendingMode: blendingMode,
                    emphasized: emphasized
                )
            }
        }
    }
}

#endif
