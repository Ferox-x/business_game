import React, { useEffect, useState } from "react"
import "./createGameStyles/checkBoxAttributeList.scss"
import CheckboxAttribute from "./checkboxAttribute"
import { useDispatch } from "react-redux"
import { CreateGameApi } from "../api/createGameApi"

function CheckboxAttributeList({ setValue, ...props }) {
	const dispatch = useDispatch()

	const [attributes, setAttributes] = useState([])

	useEffect(() => {
		new CreateGameApi().getCoordinatorAttributes().then((data) => {
			setAttributes(data)
		})
	}, [])

	return (
		<div className={"checkbox_attribute_list_content"}>
			{attributes.map((attribute, index) => {
				return <CheckboxAttribute change={setValue} key={index} text={attribute[1]} />
			})}
		</div>
	)
}

export default CheckboxAttributeList
