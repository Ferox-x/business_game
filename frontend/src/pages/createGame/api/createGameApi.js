import { getAxiosInstanceAuth } from "../../../actions/axios_config"

export class CreateGameApi {
	constructor(dispatch) {
		this.dispatch = dispatch
	}

	async getCoordinatorAttributes() {
		const axiosInstanceAuth = getAxiosInstanceAuth()

		return await axiosInstanceAuth
			.get("api/coordinator/attributes")
			.then((response) => {
				return response.data
			})
	}

	async postCreateGame(data) {
		const axiosInstanceAuth = getAxiosInstanceAuth()

		return await axiosInstanceAuth.post("api/game/start", { data })
	}
}
