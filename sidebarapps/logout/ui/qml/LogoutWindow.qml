import QtQuick 2.11
import QtQuick.Controls 2.2
import QtQuick.Window 2.3

ApplicationWindow {
    id: logoutWindow

    visible: true
    width: screen.width
    height: screen.height
    color: "transparent"
    flags: Qt.ToolTip | Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint

    FontLoader {
        id: fontLoader

        name: "Red Ring"
    }

    background: Rectangle {
        anchors.fill: parent
        color: "transparent"

        MouseArea {
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            onClicked: close()
        }

        Rectangle {
            anchors.centerIn: parent
            color: "#ffffff"
            width: 312
            height: 236
            z: 1
            opacity: 1
            radius: 4

            Image {
                id: exitIcon

                source: "qrc:/ui/icons/exit_icon.svg"
                visible: true

                anchors {
                    top: parent.top
                    topMargin: 16
                    horizontalCenter: parent.horizontalCenter
                }

            }

            Text {
                anchors.centerIn: parent
                width: parent.height - 32
                height: parent.height - 32
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                renderType: Text.NativeRendering
                wrapMode: Text.WordWrap
                color: "#333333"
                text: qsTr("Вы уверены, что хотите завершить сеанс?")

                font {
                    family: fontLoader.name
                    pixelSize: 16
                }

            }

            MouseArea {
                anchors.fill: parent
            }

            Rectangle {
                id: cancelButton

                width: 132
                height: 44
                radius: 4
                color: "#cfe1f5"

                anchors {
                    left: parent.left
                    bottom: parent.bottom
                    leftMargin: 16
                    bottomMargin: 16
                }

                Text {
                    anchors.centerIn: parent
                    renderType: Text.NativeRendering
                    color: "#036cdf"
                    text: qsTr("Отмена")

                    font {
                        weight: Font.Medium
                        capitalization: Font.AllUppercase
                        family: fontLoader.name
                        pixelSize: 14
                    }

                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onEntered: parent.color = "#b0cdec"
                    onExited: parent.color = "#cfe1f5"
                    onClicked: close()
                }

            }

            Rectangle {
                id: logoutButton

                width: 132
                height: 44
                radius: 4
                color: "#5ea2ff"

                anchors {
                    right: parent.right
                    bottom: parent.bottom
                    rightMargin: 16
                    bottomMargin: 16
                }

                Text {
                    anchors.centerIn: parent
                    renderType: Text.NativeRendering
                    color: "#ffffff"
                    text: qsTr("Завершить")

                    font {
                        weight: Font.Medium
                        capitalization: Font.AllUppercase
                        family: fontLoader.name
                        pixelSize: 14
                    }

                }

                MouseArea {
                    id: exitArea

                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onEntered: parent.color = "#4a90e2"
                    onExited: parent.color = "#5ea2ff"
                    onPressed: parent.color = "#2e4059"
                    onClicked: {
                        cursorShape = Qt.BusyCursor;
                        sessionKiller.killSession();
                    }
                }

            }

        }

        Rectangle {
            anchors.fill: parent
            color: "#1b1b1d"
            opacity: 0.5
            z: 0
        }

    }

}
