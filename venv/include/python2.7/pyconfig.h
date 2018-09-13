#if defined(__linux__)
# if defined(__x86_64__) && defined(__LP64__)
#  include <x86_64-linux-gnu/python2.7/pyconfig.h>
# elif defined(__x86_64__) && defined(__ILP32__)
#  include <x86_64-linux-gnux32/python2.7/pyconfig.h>
# elif defined(__i386__)
#  include <i386-linux-gnu/python2.7/pyconfig.h>
# elif defined(__aarch64__) && defined(__AARCH64EL__)
#  if defined(__ILP32__)
#  include <aarch64_ilp32-linux-gnu/python2.7/pyconfig.h>
#  else
#  include <aarch64-linux-gnu/python2.7/pyconfig.h>
#  endif
# elif defined(__aarch64__) && defined(__AARCH64EB__)
#  if defined(__ILP32__)
#  include <aarch64_be_ilp32-linux-gnu/python2.7/pyconfig.h>
#  else
#  include <aarch64_be-linux-gnu/python2.7/pyconfig.h>
#  endif
# elif defined(__alpha__)
#  include <alpha-linux-gnu/python2.7/pyconfig.h>
# elif defined(__ARM_EABI__) && defined(__ARM_PCS_VFP)
#  if defined(__ARMEL__)
#  include <arm-linux-gnueabihf/python2.7/pyconfig.h>
#  else
#  include <armeb-linux-gnueabihf/python2.7/pyconfig.h>
#  endif
# elif defined(__ARM_EABI__) && !defined(__ARM_PCS_VFP)
#  if defined(__ARMEL__)
#  include <arm-linux-gnueabi/python2.7/pyconfig.h>
#  else
#  include <armeb-linux-gnueabi/python2.7/pyconfig.h>
#  endif
# elif defined(__hppa__)
#  include <hppa-linux-gnu/python2.7/pyconfig.h>
# elif defined(__ia64__)
#  include <ia64-linux-gnu/python2.7/pyconfig.h>
# elif defined(__m68k__) && !defined(__mcoldfire__)
#  include <m68k-linux-gnu/python2.7/pyconfig.h>
# elif defined(__mips_hard_float) && defined(__mips_isa_rev) && (__mips_isa_rev >=6) && defined(_MIPSEL)
#  if _MIPS_SIM == _ABIO32
#   include <mipsisa32r6el-linux-gnu/python2.7/pyconfig.h>
#  elif _MIPS_SIM == _ABIN32
#   include <mipsisa64r6el-linux-gnuabin32/python2.7/pyconfig.h>
#  elif _MIPS_SIM == _ABI64
#   include <mipsisa64r6el-linux-gnuabi64/python2.7/pyconfig.h>
#  else
#   error unknown multiarch location for pyconfig.h
#  endif
# elif defined(__mips_hard_float) && defined(__mips_isa_rev) && (__mips_isa_rev >=6)
#  if _MIPS_SIM == _ABIO32
#   include <mipsisa32r6-linux-gnu/python2.7/pyconfig.h>
#  elif _MIPS_SIM == _ABIN32
#   include <mipsisa64r6-linux-gnuabin32/python2.7/pyconfig.h>
#  elif _MIPS_SIM == _ABI64
#   include <mipsisa64r6-linux-gnuabi64/python2.7/pyconfig.h>
#  else
#   error unknown multiarch location for pyconfig.h
#  endif
# elif defined(__mips_hard_float) && defined(_MIPSEL)
#  if _MIPS_SIM == _ABIO32
#   include <mipsel-linux-gnu/python2.7/pyconfig.h>
#  elif _MIPS_SIM == _ABIN32
#   include <mips64el-linux-gnuabin32/python2.7/pyconfig.h>
#  elif _MIPS_SIM == _ABI64
#   include <mips64el-linux-gnuabi64/python2.7/pyconfig.h>
#  else
#   error unknown multiarch location for pyconfig.h
#  endif
# elif defined(__mips_hard_float)
#  if _MIPS_SIM == _ABIO32
#   include <mips-linux-gnu/python2.7/pyconfig.h>
#  elif _MIPS_SIM == _ABIN32
#   include <mips64-linux-gnuabin32/python2.7/pyconfig.h>
#  elif _MIPS_SIM == _ABI64
#   include <mips64-linux-gnuabi64/python2.7/pyconfig.h>
#  else
#   error unknown multiarch location for pyconfig.h
#  endif
# elif defined(__or1k__)
#  include <or1k-linux-gnu/python2.7/pyconfig.h>
# elif defined(__powerpc__) && defined(__SPE__)
#  include <powerpc-linux-gnuspe/python2.7/pyconfig.h>
# elif defined(__powerpc64__)
#  if defined(__LITTLE_ENDIAN__)
#    include <powerpc64le-linux-gnu/python2.7/pyconfig.h>
#  else
#    include <powerpc64-linux-gnu/python2.7/pyconfig.h>
#  endif
# elif defined(__powerpc__)
#  include <powerpc-linux-gnu/python2.7/pyconfig.h>
# elif defined(__s390x__)
#  include <s390x-linux-gnu/python2.7/pyconfig.h>
# elif defined(__s390__)
#  include <s390-linux-gnu/python2.7/pyconfig.h>
# elif defined(__sh__) && defined(__LITTLE_ENDIAN__)
#  include <sh4-linux-gnu/python2.7/pyconfig.h>
# elif defined(__sparc__) && defined(__arch64__)
#  include <sparc64-linux-gnu/python2.7/pyconfig.h>
# elif defined(__sparc__)
#  include <sparc-linux-gnu/python2.7/pyconfig.h>
# elif defined(__riscv)
#  if __riscv_xlen == 64
#    include <riscv64-linux-gnu/python2.7/pyconfig.h>
#  else
#    include <riscv32-linux-gnu/python2.7/pyconfig.h>
#  endif
# else
#   error unknown multiarch location for pyconfig.h
# endif
#elif defined(__FreeBSD_kernel__)
# if defined(__LP64__)
#  include <x86_64-kfreebsd-gnu/python2.7/pyconfig.h>
# elif defined(__i386__)
#  include <i386-kfreebsd-gnu/python2.7/pyconfig.h>
# else
#   error unknown multiarch location for pyconfig.h
# endif
#elif defined(__gnu_hurd__)
# include <i386-gnu/python2.7/pyconfig.h>
#else
# error unknown multiarch location for pyconfig.h
#endif
