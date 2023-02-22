import React from "react"
import "../../generic/profileGenericStyles/attribute.scss"

function PlayerAttribute({ attribute }) {
	return (
		<div className={"user_attribute"}>
			<p className="user_attribute_item">{attribute.attribute}:</p>
			<p className="user_attribute_item user_attribute_value">{attribute.value}</p>
		</div>
	)
}

export default PlayerAttribute
