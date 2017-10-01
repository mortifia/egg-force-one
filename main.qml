import QtQuick 2.2
import QtQuick.Controls 1.0
import QtQuick.Window 2.0


Window {
    width: 480
    height: 800
    visible: true
    color: "#4f4f4f"
    id: home

    Text {
        id: text1
        x: 0
        y: 0
        width: 480
        height: 50
        color: "#ffffff"
        text: temp0
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        font.pixelSize: 24
    }
}
