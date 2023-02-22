import React from "react"
import "../../generic/genericEditStyles/formFullName.scss"
import FormLabel from "../../components/formLabel"

function FormFullName({ fullName, setFullname, ...props }) {
	return (
		<>
			<div className="form_full_name">
				<FormLabel
					variableName={"last_name"}
					value={fullName}
					setValue={setFullname}
					label={"Фамилия"}
					type={"text"}
					placeholder={"Не указана"}
				/>
				<FormLabel
					variableName={"first_name"}
					value={fullName}
					setValue={setFullname}
					label={"Имя"}
					type={"text"}
					placeholder={"Не указано"}
				/>
				<FormLabel
					variableName={"patronymic"}
					value={fullName}
					setValue={setFullname}
					label={"Отчество"}
					type={"text"}
					placeholder={"Не указано"}
				/>
			</div>
		</>
	)
}

export default FormFullName
