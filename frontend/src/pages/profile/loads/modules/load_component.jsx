import React from "react"
import "./loads_styles/load_component.scss"

function LoadComponent(props) {
	return (
		<div className={"load_component"}>
			<div className="load_label"></div>
			<div className="load_input"></div>
		</div>
	)
}

export default LoadComponent
