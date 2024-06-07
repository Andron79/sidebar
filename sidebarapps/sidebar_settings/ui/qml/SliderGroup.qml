import QtQuick 2.7
import QtQuick.Controls 2.2

Rectangle {
    id: sliderGroup

    anchors.fill: parent
    color: "transparent"

    VerticalSlider {
        id: rightSlider

        width: Styles.sliderWidth
        height: monitorScreen.height
        value: root.sliderPosition
        radius: Styles.sliderRadius
        wheelEnabled: true
        backgroundColor: "transparent"
        visible: monitorSide === Main.MonitorSide.Right
        y: Styles.monitorTop
        handleColor: Styles.settingsHandleColor
        maskColor: "transparent"
        onMoved: {
            root.sliderPosition = rightSlider.position
            monitorModel.set_sidebar_settings(root.monitorID, root.monitorSide,
                                              root.sliderPosition)
        }

        anchors {
            rightMargin: Styles.sliderSideMargin
            right: parent.right
        }

        border {
            color: Styles.sliderBorderColor
            width: Styles.sliderBorderWith
        }
    }

    VerticalSlider {
        id: leftSlider

        width: Styles.sliderWidth
        height: monitorScreen.height
        value: root.sliderPosition
        radius: Styles.sliderRadius
        wheelEnabled: true
        backgroundColor: "transparent"
        visible: monitorSide === Main.MonitorSide.Left
        y: Styles.monitorTop
        handleColor: Styles.settingsHandleColor
        maskColor: "transparent"
        onMoved: {
            root.sliderPosition = leftSlider.position
            monitorModel.set_sidebar_settings(root.monitorID, root.monitorSide,
                                              root.sliderPosition)
        }

        anchors {
            leftMargin: Styles.sliderSideMargin
            left: parent.left
        }

        border {
            color: Styles.sliderBorderColor
            width: Styles.sliderBorderWith
        }
    }

    HorizontalSlider {
        id: topSlider

        width: monitorScreen.height
        height: Styles.sliderWidth
        value: root.sliderPosition
        visible: monitorSide === Main.MonitorSide.Top
        radius: Styles.sliderRadius
        wheelEnabled: true
        backgroundColor: "transparent"
        y: Styles.monitorBottom
        handleColor: Styles.settingsHandleColor
        maskColor: "transparent"
        onMoved: {
            root.sliderPosition = topSlider.position
            monitorModel.set_sidebar_settings(root.monitorID, root.monitorSide,
                                              root.sliderPosition)
        }

        anchors {
            horizontalCenter: parent.horizontalCenter
            centerIn: monitorScreen.centerIn
        }

        border {
            color: Styles.sliderBorderColor
            width: Styles.sliderBorderWith
        }
    }

    HorizontalSlider {
        id: bottomSlider

        width: monitorScreen.height
        height: Styles.sliderWidth
        value: root.sliderPosition
        visible: monitorSide === Main.MonitorSide.Bottom
        radius: Styles.sliderRadius
        wheelEnabled: true
        backgroundColor: "transparent"
        handleColor: Styles.settingsHandleColor
        maskColor: "transparent"
        onMoved: {
            root.sliderPosition = bottomSlider.position
            monitorModel.set_sidebar_settings(root.monitorID, root.monitorSide,
                                              root.sliderPosition)
        }

        anchors {
            horizontalCenter: parent.horizontalCenter
            bottomMargin: Styles.sliderBottomMargin
            bottom: parent.bottom
        }

        border {
            color: Styles.sliderBorderColor
            width: Styles.sliderBorderWith
        }
    }
}
