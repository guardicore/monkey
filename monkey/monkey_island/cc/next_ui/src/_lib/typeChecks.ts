export function instanceOfError(object: any): object is Error {
    return 'message' in object && 'name' in object && 'stack' in object;
}
