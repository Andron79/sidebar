import QtGraphicalEffects 1.0
import QtQuick 2.7
import QtQuick.Controls 2.2

Slider {
    id: slider

    property alias maskColor: mask.color
    property alias handleColor: handle.color
    property alias backgroundColor: background.color
    property alias radius: background.radius
    property alias border: background.border

    orientation: Qt.Vertical

    background: Rectangle {
        id: background

        anchors.fill: parent

        Rectangle {
            id: _mask

            color: "#000000"
            radius: parent.radius
            anchors.fill: parent
            visible: false
        }

        Item {
            anchors.fill: _mask

            layer {
                enabled: true

                effect: OpacityMask {
                    maskSource: _mask
                }

            }

            Rectangle {
                id: mask

                width: parent.width
                height: slider.height
                y: slider.visualPosition * (slider.height - slider.width)
                radius: height / 2
            }

        }

    }

    handle: Rectangle {
        id: handle

        y: slider.visualPosition * (slider.availableHeight)
        radius: implicitHeight / 2
        implicitHeight: slider.width
        implicitWidth: slider.width
    }

}
