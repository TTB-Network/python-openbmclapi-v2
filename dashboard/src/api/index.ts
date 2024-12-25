export interface Config {
    language: string
    clusterId: string
    clusterSecret: string
    password: string
    username: string
    byoc: boolean
    host?: string
}

export async function postConfig() {

}