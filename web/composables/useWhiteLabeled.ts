export function useWhiteLabeled() {
  const getCurrentHost = () => {
    const url = useRequestURL()
    return `${url.protocol}//${url.host}`
  }

  return {
    getCurrentHost
  }
}