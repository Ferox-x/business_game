import React from "react"
import "../../generic/profileGenericStyles/attributeList.scss"
import PlayerAttribute from "./playerAttribute"

function PlayerAttributeList({ attributes, ...props }) {
	return (
		<div className={"user_attribute_list"}>
			{attributes.map((attribute, index) => {
				return <PlayerAttribute key={index} attribute={attribute} />
			})}
		</div>
	)
}

export default PlayerAttributeList
