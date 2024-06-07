import QtGraphicalEffects 1.0
import QtQuick 2.11
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.12
import QtQuick.Window 2.2

ApplicationWindow {
    id: window

    enum MonitorSide {
        Right,
        Left,
        Top,
        Bottom
    }

    property string defaultImage: statusIcon
    readonly property int defaultRadius: 6
    readonly property int retractedWidth: 20
    readonly property int retractedHeight: 40
    readonly property int retractedHorizontaldWidth: 40
    readonly property int retractedHorizontalHeight: 20
    readonly property int protractedWidth: 40
    property int monitorID: sidebarPosition.monitor_id
    property int monitorSide: sidebarPosition.monitor_side

    function getSidebarX(side) {
        var virtualScreenX = screenGeometry[monitorID].x
        var primaryScreenX = screenGeometry[monitorID].width - width
        switch (side) {
        case Main.MonitorSide.Left:
            return virtualScreenX
        case Main.MonitorSide.Right:
            return primaryScreenX + virtualScreenX
        default:
            return primaryScreenX * sidebarPosition.slider_position + virtualScreenX
        }
    }

    function getSidebarY(side) {
        var virtualScreenY = screenGeometry[monitorID].y
        var primaryScreenY = screenGeometry[monitorID].height - height
        switch (side) {
        case Main.MonitorSide.Top:
            return virtualScreenY
        case Main.MonitorSide.Bottom:
            return primaryScreenY + virtualScreenY
        default:
            return primaryScreenY * (1 - sidebarPosition.slider_position)
        }
    }

    function getSidebarRetractedState(side) {
        switch (side) {
        case Main.MonitorSide.Top:
            return "retractedTop"
        case Main.MonitorSide.Bottom:
            return "retractedBottom"
        default:
            return "retracted"
        }
    }

    function getSidebarProtractedState(side) {
        switch (side) {
        case Main.MonitorSide.Top:
            return "protractedHorizontal"
        case Main.MonitorSide.Bottom:
            return "protractedHorizontal"
        default:
            return "protracted"
        }
    }

    function getIconPath(icon) {
        if (icon)
            if (icon.startsWith("qrc:/"))
                return icon
            else
                return "file://" + icon
    }

    title: qsTr("sidebar")
    color: "transparent"
    visible: true
    flags: Qt.ToolTip | Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus
           | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint
    width: background.width + 10
    height: background.height + 10
    x: getSidebarX(monitorSide)
    y: getSidebarY(monitorSide)
    LayoutMirroring.enabled: monitorSide === Main.MonitorSide.Left
    LayoutMirroring.childrenInherit: true
    Component.onCompleted: {
        background.state = getSidebarRetractedState(monitorSide)
    }

    Timer {
        id: hideTimer

        onTriggered: {
            background.state = getSidebarRetractedState(monitorSide)
        }
        interval: 1200
        repeat: false
        running: false
    }

    Timer {
        id: raiseTimer

        onTriggered: {
            window.raise()
        }
        interval: 10000
        repeat: true
        running: true
    }

    Connections {
        target: window

        function onMonitorSideChanged() {
            background.state = getSidebarRetractedState(monitorSide)
        }
    }
    Rectangle {
        id: background

        radius: defaultRadius
        height: buttons.height
        width: protractedWidth
        color: "#3F3F3F"
        onStateChanged: {
            console.log("State: " + state)
        }
        states: [
            State {
                name: "retracted"

                PropertyChanges {
                    target: background
                    width: retractedWidth
                    height: retractedHeight
                }

                PropertyChanges {
                    target: background
                    color: "#3F3F3F"
                }

                PropertyChanges {
                    target: background
                    anchors.rightMargin: 0
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                }
            },
            State {
                name: "retractedBottom"

                PropertyChanges {
                    target: background
                    width: retractedHorizontaldWidth
                    height: retractedHorizontalHeight
                    radius: defaultRadius
                }

                PropertyChanges {
                    target: background
                    color: "#3F3F3F"
                }

                PropertyChanges {
                    target: background
                    anchors.bottomMargin: 0
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: undefined
                }

                //                PropertyChanges {
                //                    target: buttons
                //                    anchors.bottomMargin: 0
                //                    height: retractedHorizontalHeight
                //                    anchors.top: parent.top
                //                }
            },

            State {
                name: "retractedTop"

                PropertyChanges {
                    target: background
                    width: retractedHorizontaldWidth
                    height: retractedHorizontalHeight
                    radius: defaultRadius
                }

                PropertyChanges {
                    target: background
                    color: "#3F3F3F"
                }

                PropertyChanges {
                    target: background
                    anchors.topMargin: 0
                    anchors.verticalCenter: parent.verticalCenter
                }

                //                PropertyChanges {
                //                    target: buttons
                //                    anchors.topMargin: 0
                //                    height: retractedHorizontalHeight
                //                    anchors.bottom: parent.bottom
                //                }
            },

            State {
                name: "protracted"

                PropertyChanges {
                    target: background
                    width: protractedWidth
                    height: buttons.childrenRect.height
                }

                PropertyChanges {
                    target: background
                    anchors.rightMargin: 0
                    anchors.verticalCenter: parent.verticalCenter
                }
            },
            State {
                name: "protractedHorizontal"

                PropertyChanges {
                    target: background
                    width: sidebarListItem.contentWidth
                    height: buttons.childrenRect.height
                }

                PropertyChanges {
                    target: background
                    anchors.topMargin: 0
                    anchors.bottomMargin: 0
                    anchors.verticalCenter: parent.verticalCenter
                }

                PropertyChanges {
                    target: sideBar
                    height: retractedHeight
                }
            }
        ]

        MouseArea {
            id: clickArea

            property int prevY: 0

            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            onPressed: prevY = mouse.y
            onReleased: {
                if (background.state !== getSidebarProtractedState(monitorSide)
                        && containsMouse)
                    background.state = getSidebarProtractedState(monitorSide)
            }
        }

        Column {
            id: buttons

            width: parent.width + defaultRadius

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
            }
            Rectangle {
                id: retractedIcon

                height: background.state !== getSidebarProtractedState(
                            monitorSide) ? protractedWidth : 0
                width: parent.width
                radius: defaultRadius
                color: "#3F3F3F"
                clip: false

                MouseArea {
                    id: retractedIconArea

                    cursorShape: Qt.PointingHandCursor
                    propagateComposedEvents: true
                    acceptedButtons: Qt.NoButton
                    hoverEnabled: true
                    height: protractedWidth
                    width: parent.width
                    onEntered: parent.color = "#1B1B1D"
                    onExited: parent.color = "#3F3F3F"

                    anchors {
                        top: parent.top
                        left: parent.left
                    }
                }

                Image {
                    id: retractedIconImage

                    visible: background.state !== getSidebarProtractedState(
                                 monitorSide)
                    source: defaultImage.startsWith(
                                "qrc:/") ? defaultImage : "file://" + defaultImage
                    anchors {
                        left: parent.left
                        top: parent.top
                        centerIn: parent
                    }
                }
            }

            Rectangle {
                id: sideBar

                height: sidebarListItem.childrenRect.height
                width: parent.width
                visible: background.state === getSidebarProtractedState(
                             monitorSide)
                radius: defaultRadius
                color: "transparent"

                ListView {
                    id: sidebarListItem

                    model: sidebarModel
                    height: childrenRect.height
                    width: childrenRect.width
                    orientation: (background.state == "protractedHorizontal") ? ListView.Horizontal : ListView.Vertical

                    delegate: Rectangle {
                        id: itemRectangle

                        color: "transparent"
                        radius: defaultRadius
                        width: iconImage.width + 16
                        height: iconImage.height + 16
                        clip: true
                        Connections {
                            target: sidebarModel
                            function onDataChanged() {
                                iconImage.source = getIconPath(icon)
                            }
                        }

                        Image {
                            id: iconImage
                            source: {

                                if (background.state == "protractedHorizontal")
                                    if (icon_horizontal)
                                        iconImage.source = getIconPath(
                                                    icon_horizontal)
                                    else
                                        iconImage.source = getIconPath(icon)
                                if (background.state == "protracted")
                                    iconImage.source = getIconPath(icon)
                            }
                            anchors {
                                left: parent.left
                                centerIn: parent
                                horizontalCenterOffset: -defaultRadius / 2
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            propagateComposedEvents: true
                            onClicked: {
                                sidebarModel.execute(command)
                            }
                            onPressed: {
                                if (background.state !== getSidebarProtractedState(
                                            monitorSide))
                                    mouse.accepted = false
                            }
                            onEntered: {
                                itemRectangle.color = "#1B1B1D"
                                hideTimer.stop()
                            }
                            onExited: {
                                itemRectangle.color = "#3F3F3F"
                                hideTimer.restart()
                            }
                        }
                    }
                }
            }
        }

        transitions: Transition {
            to: getSidebarProtractedState(monitorSide)
            reversible: true

            ParallelAnimation {
                NumberAnimation {
                    properties: "x"
                    duration: 100
                }

                NumberAnimation {
                    properties: "height"
                    duration: 100
                }

                NumberAnimation {
                    properties: "width"
                    duration: 100
                }

                NumberAnimation {
                    properties: "anchors.topMargin"
                    duration: 100
                }

                NumberAnimation {
                    properties: "opacity"
                    duration: 0
                }

                NumberAnimation {
                    properties: "source"
                    duration: 0
                }
            }
        }
    }

    DropShadow {
        anchors.fill: background
        horizontalOffset: 0
        verticalOffset: 0
        radius: 10
        color: "#80000000"
        samples: 16
        source: background
        cached: true
    }
}
