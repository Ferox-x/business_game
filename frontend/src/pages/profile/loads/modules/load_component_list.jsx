import React from "react"
import "./loads_styles/load_component_list.scss"
import LoadComponent from "./load_component"

function LoadComponentList(props) {
	return (
		<div className={"loads_component_list"}>
			<LoadComponent />
			<LoadComponent />
			<LoadComponent />
			<LoadComponent />
			<LoadComponent />
			<LoadComponent />
		</div>
	)
}

export default LoadComponentList
