const defaultMinHeight = 50
const defaultMaxHeight = 300
const defaultSubcomponentHeight = 15

export function getComponentHeight(subcomponentCount,
                                   subcomponentHeight = defaultSubcomponentHeight,
                                   minHeight = defaultMinHeight,
                                   maxHeight = defaultMaxHeight) {
  let height = subcomponentHeight * subcomponentCount;
  if (height > maxHeight)
    height = maxHeight
  else if (height < minHeight)
    height = minHeight

  return height
}
