import React from "react"
import "../../../generic/profileGenericStyles/attribute.scss"
import "./coordinatorComponentsStyle/coordinatorAttribute.scss"

function CoordinatorAttribute({ attribute, ...props }) {
	return (
		<div className={"user_attribute"}>
			<p className="user_attribute__item icon_item">{attribute.attribute}</p>
			<p className="user_attribute__item user_attribute__value">{attribute.value}</p>
		</div>
	)
}

export default CoordinatorAttribute
