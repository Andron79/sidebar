import QtQuick 2.7
import QtQuick.Controls 2.2

Rectangle {
    id: radioScreen

    radius: Styles.defaultRadius
    y: monitorScreen.y - Styles.radioIndicatorImplicitHeight / 2
    x: monitorScreen.x - Styles.radioIndicatorImplicitWidth / 2
    width: monitorScreen.width + Styles.radioIndicatorImplicitHeight
    height: monitorScreen.height + Styles.radioIndicatorImplicitWidth
    color: "transparent"
    visible: true

    RadioButton {
        id: rightPosition

        anchors.verticalCenter: parent.verticalCenter
        anchors.right: parent.right
        checked: monitorSide === Main.MonitorSide.Right
        ButtonGroup.group: radioGroup
        visible: visibleSides.includes(Main.MonitorSide.Right)
        onClicked: {
            root.monitorSide = Main.MonitorSide.Right
            monitorModel.set_sidebar_settings(root.monitorID, root.monitorSide,
                                              root.sliderPosition)
        }

        indicator: Rectangle {
            implicitWidth: Styles.radioIndicatorImplicitWidth
            implicitHeight: Styles.radioIndicatorImplicitHeight
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            radius: Styles.radioIndicatorRadius
            color: Styles.radioButtonBackgroundColor
            border.color: rightPosition.checked ? Styles.radioButtonCheckedColor : Styles.radioButtonUncheckedColor

            Rectangle {
                width: Styles.radioIndicatorImplicitWidth / 2
                height: Styles.radioIndicatorImplicitHeight / 2
                x: Styles.radioButtonRectangleX
                y: Styles.radioButtonRectangleY
                radius: Styles.radioButtonRectangleRadius
                color: rightPosition.checked ? Styles.radioButtonCheckedColor : Styles.radioButtonCheckedColor
                visible: rightPosition.checked
            }
        }
    }

    RadioButton {
        id: leftPosition

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: root.monitorBorders
        ButtonGroup.group: radioGroup
        checked: monitorSide === Main.MonitorSide.Left
        visible: visibleSides.includes(Main.MonitorSide.Left)
        onClicked: {
            root.monitorSide = Main.MonitorSide.Left
            monitorModel.set_sidebar_settings(root.monitorID, root.monitorSide,
                                              root.sliderPosition)
        }

        indicator: Rectangle {
            implicitWidth: Styles.radioIndicatorImplicitWidth
            implicitHeight: Styles.radioIndicatorImplicitHeight
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            radius: Styles.radioIndicatorRadius
            color: Styles.radioButtonBackgroundColor
            border.color: leftPosition.checked ? Styles.radioButtonCheckedColor : Styles.radioButtonUncheckedColor

            Rectangle {
                width: Styles.radioIndicatorImplicitWidth / 2
                height: Styles.radioIndicatorImplicitHeight / 2
                x: Styles.radioButtonRectangleX
                y: Styles.radioButtonRectangleY
                radius: Styles.radioButtonRectangleRadius
                color: leftPosition.checked ? Styles.radioButtonCheckedColor : Styles.radioButtonCheckedColor
                visible: leftPosition.checked
            }
        }
    }

    RadioButton {
        id: topPosition

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        ButtonGroup.group: radioGroup
        checked: monitorSide === Main.MonitorSide.Top
        visible: visibleSides.includes(Main.MonitorSide.Top)
        onClicked: {
            root.monitorSide = Main.MonitorSide.Top
            monitorModel.set_sidebar_settings(root.monitorID, root.monitorSide,
                                              root.sliderPosition)
        }

        indicator: Rectangle {
            implicitWidth: Styles.radioIndicatorImplicitWidth
            implicitHeight: Styles.radioIndicatorImplicitHeight
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            radius: Styles.radioIndicatorRadius
            color: Styles.radioButtonBackgroundColor
            border.color: topPosition.checked ? Styles.radioButtonCheckedColor : Styles.radioButtonUncheckedColor

            Rectangle {
                width: Styles.radioIndicatorImplicitWidth / 2
                height: Styles.radioIndicatorImplicitHeight / 2
                x: Styles.radioButtonRectangleX
                y: Styles.radioButtonRectangleY
                radius: Styles.radioButtonRectangleRadius
                color: topPosition.checked ? Styles.radioButtonCheckedColor : Styles.radioButtonCheckedColor
                visible: topPosition.checked
            }
        }
    }

    RadioButton {
        id: bottomPosition

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        ButtonGroup.group: radioGroup
        checked: monitorSide === Main.MonitorSide.Bottom
        visible: visibleSides.includes(Main.MonitorSide.Bottom)
        onClicked: {
            root.monitorSide = Main.MonitorSide.Bottom
            monitorModel.set_sidebar_settings(root.monitorID, root.monitorSide,
                                              root.sliderPosition)
        }

        indicator: Rectangle {
            implicitWidth: Styles.radioIndicatorImplicitWidth
            implicitHeight: Styles.radioIndicatorImplicitHeight
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            radius: Styles.radioIndicatorRadius
            color: Styles.radioButtonBackgroundColor
            border.color: bottomPosition.checked ? Styles.radioButtonCheckedColor : Styles.radioButtonUncheckedColor

            Rectangle {
                width: Styles.radioIndicatorImplicitWidth / 2
                height: Styles.radioIndicatorImplicitHeight / 2
                x: Styles.radioButtonRectangleX
                y: Styles.radioButtonRectangleY
                radius: Styles.radioButtonRectangleRadius
                color: bottomPosition.checked ? Styles.radioButtonCheckedColor : Styles.radioButtonCheckedColor
                visible: bottomPosition.checked
            }
        }
    }
}
