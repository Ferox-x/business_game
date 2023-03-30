import React, { useEffect, useState } from "react"
import "./editStyles/formAttributes.scss"

import InvisibleLabel from "./invisibleLabel"
import FormLabelAttribute from "../components/formLabelAttribute"
import Loads from "../../profile/loads/loads"
import { PlayerProfileApi } from "../api/playerEditApi"

function FormAttributes({ attributesAndValue, setAttributesAndValue, ...props }) {
	const [attributes, setAttributes] = useState([false])

	useEffect(() => {
		new PlayerProfileApi().getAttributes().then((attributes) => {
			setAttributes(attributes)
		})
	}, [])

	function renderAttributes() {
		return attributes.map((attribute, index) => {
			return (
				<FormLabelAttribute
					key={index}
					attributesAndValue={attributesAndValue}
					setAttributesAndValue={setAttributesAndValue}
					htmlFor={attribute[0]}
					label={attribute[1]}
					type={"text"}
					id={attribute[0]}
					placeholder={"Заполните поле"}
				/>
			)
		})
	}

	function renderLoads() {
		return <Loads />
	}

	return (
		<div className="form_attributes">
			{attributes[0] ? renderAttributes() : renderLoads()}
			<InvisibleLabel />
		</div>
	)
}

export default FormAttributes
