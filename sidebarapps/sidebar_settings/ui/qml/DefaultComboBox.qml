import QtQuick 2.7
import QtQuick.Controls 2.2

ComboBox {
    id: monitorComboBox

    model: monitorModel
    height: 16

    anchors {
        top: parent.top
        horizontalCenter: parent.horizontalCenter
        topMargin: 50
        leftMargin: 5
    }

    background: MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: mouse.accepted = false
        onPressed: mouse.accepted = false
    }

    contentItem: Text {
        width: contentWidth < 300 ? contentWidth : 300
        color: "#ffffff"
        font.pixelSize: 13
        font.family: Styles.fontFamily
        text: "Выбрать монитор"
    }

    delegate: MouseArea {

        hoverEnabled: true
        width: defaultDeviceId.width + 20
        height: 24
        onClicked: {
            root.monitorID = monitor_id
            monitorModel.set_sidebar_settings(root.monitorID, root.monitorSide,
                                              root.sliderPosition)
            monitorComboBox.popup.close()
        }

        Rectangle {
            width: monitorComboBoxList.width - 4
            color: containsMouse ? "#444444" : "transparent"

            anchors {
                top: parent.top
                bottom: parent.bottom
                left: parent.left
                leftMargin: 2
            }
        }

        Text {
            id: defaultDeviceId

            x: parent.x + 12
            width: implicitWidth < 400 ? implicitWidth : 400
            color: "#ffffff"
            font.pixelSize: 13
            font.family: Styles.fontFamily
            verticalAlignment: Text.AlignVCenter
            text: monitor_id + ". " + name + " " + port
            elide: Text.ElideRight

            anchors {
                top: parent.top
                bottom: parent.bottom
            }
        }
    }

    popup: Popup {
        y: monitorComboBox.height + 4
        implicitHeight: contentItem.implicitHeight + 2
        padding: 0
        clip: true

        contentItem: ListView {
            id: monitorComboBoxList

            implicitHeight: contentHeight
            implicitWidth: contentItem.childrenRect.width
            width: implicitWidth
            x: parent.x + 2
            y: parent.y + 4
            model: monitorComboBox.popup.visible ? monitorComboBox.delegateModel : null
            currentIndex: monitorComboBox.highlightedIndex
        }

        background: Rectangle {
            color: "#2e2d32"
            border.color: "#1b1b1d"
            border.width: 2
        }

        enter: Transition {}

        exit: Transition {}
    }

    indicator: Image {
        x: monitorComboBox.width
        y: 0
        width: 16
        height: 16
        source: {
            if (monitorComboBox.popup.visible)
                "qrc:/ui/icons/arrow_up.svg"
            else
                "qrc:/ui/icons/arrow_down.svg"
        }
    }
}
