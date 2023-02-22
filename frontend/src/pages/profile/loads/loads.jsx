import React from "react"
import "./loads.scss"
import LoadComponentList from "./modules/load_component_list"

function Loads(props) {
	return (
		<div className={"loads_container"}>
			<LoadComponentList />
		</div>
	)
}

export default Loads
