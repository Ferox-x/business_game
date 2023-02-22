import React from "react"
import "./modalStyles/modalCoordinatorCodeSection.scss"
import ModalCoordinatorCode from "./modalCoordinatorCode"
import ModalCoordinatorUrl from "./modalCoordinatorUrl"

function ModalCoordinatorCodeSection(props) {
	return (
		<div className={"modal_coordinator_code_section_fill"}>
			<ModalCoordinatorCode />
			<ModalCoordinatorUrl />
		</div>
	)
}

export default ModalCoordinatorCodeSection
