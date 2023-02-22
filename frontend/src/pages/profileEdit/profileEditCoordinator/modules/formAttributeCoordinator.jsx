import React from "react"
import "./editFormCoordinatorStyles/formAttributeCoordinator.scss"
import FormLabelAttribute from "../../components/formLabelAttribute"

function FormAttributeCoordinator({
	attributesAndValue,
	setAttributesAndValue,
	...props
}) {
	return (
		<div className="form_attribute_coordinator">
			<FormLabelAttribute
				attributesAndValue={attributesAndValue}
				setAttributesAndValue={setAttributesAndValue}
				htmlFor={"job_title"}
				label={"Должность"}
				type={"text"}
				id={"job_title"}
				placeholder={"Не указана"}
			/>
			<FormLabelAttribute
				attributesAndValue={attributesAndValue}
				setAttributesAndValue={setAttributesAndValue}
				htmlFor={"company"}
				label={"Компания"}
				type={"text"}
				id={"company"}
				placeholder={"Не указана"}
			/>
			<FormLabelAttribute
				attributesAndValue={attributesAndValue}
				setAttributesAndValue={setAttributesAndValue}
				htmlFor={"birthday"}
				label={"Дата рождения"}
				type={"date"}
				id={"birthday"}
				placeholder={"Не указана"}
			/>
			<FormLabelAttribute
				attributesAndValue={attributesAndValue}
				setAttributesAndValue={setAttributesAndValue}
				htmlFor={"phone_number"}
				label={"Телефон"}
				type={"tel"}
				id={"phone_number"}
				placeholder={"Не указан"}
			/>
		</div>
	)
}

export default FormAttributeCoordinator
