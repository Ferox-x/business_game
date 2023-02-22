import React from "react"
import "./coordinatorComponentsStyle/coordinatorCodeSection.scss"
import CoordinatorCode from "./coordinatorCode"
import CoordinatorUrl from "./coordinatorUrl"

function CoordinatorCodeSection(props) {
	return (
		<div className={"coordinator_code_section"}>
			<CoordinatorCode />
			<CoordinatorUrl />
		</div>
	)
}

export default CoordinatorCodeSection
