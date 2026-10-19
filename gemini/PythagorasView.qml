import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    width: 400
    height: 300
    color: "#0f172a"

    Column {
        anchors.centerIn: parent
        spacing: 10

        Text {
            text: "Pythagoras Web3 Data Viewer"
            color: "#f8fafc"
            font.pixelSize: 18
        }

        TextField {
            id: sideAInput
            placeholderText: "Enter Side A"
        }

        TextField {
            id: sideBInput
            placeholderText: "Enter Side B"
        }

        Button {
            text: "Calculate"
            onClicked: {
                var a = Number(sideAInput.text)
                var b = Number(sideBInput.text)
                var c = Math.sqrt(Math.pow(a, 2) + Math.pow(b, 2))
                resultText.text = "Result: " + c
            }
        }

        Text {
            id: resultText
            text: "Result: -"
            color: "#38bdf8"
        }
    }
}
