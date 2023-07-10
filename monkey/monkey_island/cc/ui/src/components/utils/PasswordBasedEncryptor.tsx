import AES from "crypto-js/aes";
import Utf8 from "crypto-js/enc-utf8";

export function encryptText(content: string, password: string): string {
  return AES.encrypt(content, password).toString();
}

export function decryptText(ciphertext: string, password: string): string {
  let bytes = AES.decrypt(ciphertext, password);
  return bytes.toString(Utf8);
}
