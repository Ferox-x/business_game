import React from "react"
import "../../../generic/profileGenericStyles/attributeList.scss"
import CoordinatorAttribute from "./coordinatorAttribute"

function CoordinatorAttributeList({ attributes, ...props }) {
	return (
		<div className={"attribute_list"}>
			{attributes.map((attribute, index) => {
				return <CoordinatorAttribute key={index} attribute={attribute} />
			})}
		</div>
	)
}

export default CoordinatorAttributeList
