import QtGraphicalEffects 1.0
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Window 2.2
import QtQuick.Window 2.2

ApplicationWindow {
    id: window

    property alias title: titleBar.title

    width: 1000
    height: 700
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus
    visible: true

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.NoButton
        cursorShape: Qt.ArrowCursor
    }

    MouseArea {
        property point pos

        anchors.fill: parent
        onPressed: {
            pos = Qt.point(mouse.x, mouse.y);
        }
        onPositionChanged: {
            var diff = Qt.point(mouse.x - pos.x, mouse.y - pos.y);
            ApplicationWindow.window.x += diff.x;
            ApplicationWindow.window.y += diff.y;
        }
    }

    Rectangle {
        id: background

        anchors.fill: parent
        color: Styles.backgroundColor

        TitleBar {
            id: titleBar

            window: window
            height: 52

            anchors {
                top: parent.top
                left: parent.left
                right: parent.right
            }

        }

        CloseButton {
            anchors {
                top: parent.top
                right: parent.right
            }

        }

    }

}
