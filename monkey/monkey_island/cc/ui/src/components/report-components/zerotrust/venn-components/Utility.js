export class TypographicUtilities {

  static removeAmpersand(string_) {
    return string_.replace(' & ', 'And');
  }

  static removeBrokenBar(string_) {
    return string_.replace(/\|/g, ' ');
  }

  static setTitle(string_) {
    return string_.charAt(0).toUpperCase() + string_.substr(1).toLowerCase();
  }

}
