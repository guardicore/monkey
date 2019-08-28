export class TypographicUtilities {
  static removeAmpersand(string_) {
    return string_.replace(' & ', 'And');
  }

  static removeBrokenBar(string_) {
    return string_.replace(/\|/g, ' ');
  }
}
