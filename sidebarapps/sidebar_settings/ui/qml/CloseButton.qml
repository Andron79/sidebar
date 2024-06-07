import QtQuick 2.7
import QtQuick.Controls 2.2

Rectangle {
    width: 32
    height: 32

    color: Styles.closeButtonColor

    MouseArea {
        property bool activated: false

        anchors.fill: parent
        hoverEnabled: true

        onEntered: parent.color = Styles.hoveredCloseButtonColor
        onReleased: {
            if (activated) {
                console.log("Closing sidebar-settings-...")
                Qt.quit()
            }
        }

        onPressed: {
            parent.color = Styles.pressedCloseButtonColor
            activated = true
        }

        onExited: {
            parent.color = Styles.closeButtonColor
            activated = false
        }
    }

    Image {
        anchors {
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }
        source: "qrc:/ui/icons/close.svg"

        width: 14
        height: 14
    }
}
