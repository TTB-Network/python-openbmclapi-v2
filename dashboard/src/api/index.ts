import axios from 'axios'

export interface StatsData {
    hits: number
    bytes: number
}

export interface Stats {
    hours: StatsData[]
    days: StatsData[]
    months: StatsData[]
}

export interface UserAgent {
    [ua: string]: number
}

export interface Cluster {
    _id: string
    name: string
    isEnabled: boolean
    metric?: {
        bytes: number
        hits: number
    }
}

export interface StatsRes {
    status: number
    startTime: number
    stats: Stats
    prevStats: Stats
    accesses: UserAgent
    connections: number
    memory: number
    cpu: number
    cpuType: string
    pythonVersion: string
    apiVersion: string
    version: string
}

export async function fetchStat() {
    const res = await axios.get<StatsRes>('/api/status')
    return res.data
}

export async function fetchRank() {
    const res = await axios.get<Cluster[]>('/api/rank')
    return res.data
}

function getWebSocketURL(path: string) {
    const baseURL = axios.defaults.baseURL || ''
    const url = new URL(baseURL)
    url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
    url.pathname = path
    return url.toString()
}

const ws = new WebSocket(getWebSocketURL('/ws/logs'))

ws.onmessage = function(event) {
    console.log('Received log:', event.data)
}

ws.onopen = function() {
    console.log("WebSocket connection established.")
}

ws.onclose = function() {
    console.log("WebSocket connection closed.")
}

ws.onerror = function(error) {
    console.error("WebSocket error:", error)
}
