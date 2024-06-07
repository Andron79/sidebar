pragma Singleton

import QtQuick 2.7

QtObject {
    property FontLoader fontLoader: FontLoader {
        id: fontLoader
        name: "Red Ring"
    }
    readonly property alias fontFamily: fontLoader.name

    readonly property color closeButtonColor: "#e56a56"
    readonly property color hoveredCloseButtonColor: "#d4523d"
    readonly property color pressedCloseButtonColor: "#954538"
    readonly property color backgroundColor: "#1b1b1d"

    readonly property color titleColor: "#ffffff"
    readonly property color selectedTabTextColor: "#ffffff"
    readonly property color deselectedTabTextColor: "#5ea2ff"
    readonly property int defaultRadius: 4
    readonly property int monitorBorderWidth: 4
    readonly property int monitorBorderSideMargin: 20
    readonly property int monitorBorderTopMargin: 52
    readonly property color monitorBordersColor: "#2E2D32"
    readonly property color monitorBackgroundColor: "#2E2D32"
    readonly property color monitorScreenBorderColor: "#444444"
    readonly property color monitorScreenColor: "#1B1B1D"

    readonly property int radioIndicatorRadius: 13
    readonly property int radioIndicatorImplicitWidth: 24
    readonly property int radioIndicatorImplicitHeight: 24

    readonly property int radioButtonRectangleX: 6
    readonly property int radioButtonRectangleY: 6
    readonly property int radioButtonRectangleRadius: 7

    readonly property color radioButtonBackgroundColor: "#2E2D32"
    readonly property color radioButtonCheckedColor: "#74A6FF"
    readonly property color radioButtonUncheckedColor: "#444444"
    readonly property color settingsHandleColor: "#ffffff"

    readonly property int monitorTop: 161
    readonly property int monitorLeft: 149
    readonly property int monitorBottom: 109
    readonly property int monitorRight: 149

    readonly property color sliderBorderColor: "#444444"
    readonly property int sliderRadius: 10
    readonly property int sliderBorderWith: 2
    readonly property int sliderSideMargin: 95
    readonly property int sliderBottomMargin: 55
    readonly property int sliderWidth: 12
}
