import QtGraphicalEffects 1.0
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtQuick.Window 2.14

GMWindow {
    id: root

    enum MonitorSide {
        Right,
        Left,
        Top,
        Bottom
    }

    property int monitorSide: sidebarMonitorSide
    property int monitorID: sidebarMonitorID
    property real sliderPosition: sidebarSliderPosition

    width: 578
    height: 478
    Component.onCompleted: {
        x = screenGeometry[monitorID].width / 2 - width / 2 + screenGeometry[monitorID].x
        y = screenGeometry[monitorID].height / 2 - height / 2 + screenGeometry[monitorID].y
    }

    Timer {
        id: raiseTimer

        onTriggered: {
            root.raise()
        }
        interval: 10000
        repeat: true
        running: true
    }

    ButtonGroup {
        id: radioGroup
    }

    Rectangle {
        id: monitorBackground

        width: parent.width
        height: parent.height
        color: Styles.monitorBackgroundColor

        anchors {
            fill: parent
            topMargin: Styles.monitorBorderTopMargin
            leftMargin: Styles.monitorBorderSideMargin
            bottomMargin: Styles.monitorBorderSideMargin
            rightMargin: Styles.monitorBorderSideMargin
        }

        Text {
            id: defaultDeviceLabel

            color: "#949494"
            font.pixelSize: 13
            font.family: Styles.fontFamily
            text: qsTr("Позиция сайдбара на мониторе")

            anchors {
                top: parent.top
                horizontalCenter: parent.horizontalCenter
                topMargin: Styles.monitorBorderSideMargin
                leftMargin: Styles.monitorBorderSideMargin
            }
        }

        DefaultComboBox {
            id: defaultComboBox

            visible: true
            model: monitorModel
        }

        Rectangle {
            id: monitorScreen

            radius: Styles.defaultRadius
            border.width: Styles.monitorBorderWidth
            border.color: Styles.monitorScreenBorderColor
            color: Styles.monitorScreenColor

            anchors {
                fill: parent
                topMargin: Styles.monitorTop
                leftMargin: Styles.monitorLeft
                bottomMargin: Styles.monitorBottom
                rightMargin: Styles.monitorRight
            }

            Text {
                text: qsTr(root.monitorID.toString())
                font.pixelSize: 64
                font.family: Styles.fontFamily
                color: Styles.titleColor
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        SliderGroup {}

        RadioButtonsGroup {}
    }
}
