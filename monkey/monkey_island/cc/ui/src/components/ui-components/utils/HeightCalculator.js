const defaultMinHeight = 25
const defaultMaxHeight = 250
const defaultSubcomponentHeight = 25

export function getComponentHeight(subcomponentCount,
                                   subcomponentHeight = defaultSubcomponentHeight,
                                   minHeight = defaultMinHeight,
                                   maxHeight = defaultMaxHeight) {
  let height = minHeight + (subcomponentHeight*subcomponentCount);
  if (height > maxHeight)
    height = maxHeight

  return height
}
