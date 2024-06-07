import QtQuick 2.7
import QtQuick.Controls 2.2

MouseArea {
    property variant window
    property variant cursor: Qt.point(0, 0)
    property alias title: text.text

    onPressed: cursor = Qt.point(mouseX, mouseY)
    onPositionChanged: {
        if (pressed) {
            var delta = Qt.point(mouse.x - cursor.x, mouse.y - cursor.y);
            window.x += delta.x;
            window.y += delta.y;
            cursor = Qt.point(mouse.x - delta.x, mouse.y - delta.y);
        }
    }

    Text {
        id: text

        font.pixelSize: 24
        font.family: Styles.fontFamily
        color: Styles.titleColor
        text: qsTr("Настройки положения сайдбара")

        anchors {
            top: parent.top
            left: parent.left
            topMargin: 8
            leftMargin: 20
        }

    }

}
