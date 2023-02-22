import React from "react"
import "../modules/modalStyles/modalButtonCode.scss"
import ModalSpanText from "./modalSpanText"

function ModalButtonCode(props) {
	return (
		<div className={"modal_button_coordinator_container"}>
			<div className={"modal_button_coordinator_code"}></div>
			<ModalSpanText modal={{ span: "Коп. код" }} />
		</div>
	)
}

export default ModalButtonCode
