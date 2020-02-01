# Generated from Drake.g4 by ANTLR 4.7.1
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


from antlr4.Token import CommonToken
import re
import importlib

# Allow languages to extend the lexer and parser, by loading the parser dynamically
module_path = __name__[:-5]
language_name = __name__.split('.')[-1]
language_name = language_name[:-5]  # Remove Lexer from name
LanguageParser = getattr(importlib.import_module('{}Parser'.format(module_path)), '{}Parser'.format(language_name))


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2d")
        buf.write("\u0379\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\t")
        buf.write("L\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT\4U\t")
        buf.write("U\4V\tV\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t[\4\\\t\\\4]\t]\4")
        buf.write("^\t^\4_\t_\4`\t`\4a\ta\4b\tb\4c\tc\4d\td\4e\te\4f\tf\4")
        buf.write("g\tg\4h\th\4i\ti\4j\tj\4k\tk\4l\tl\4m\tm\4n\tn\4o\to\4")
        buf.write("p\tp\4q\tq\4r\tr\4s\ts\4t\tt\4u\tu\4v\tv\4w\tw\4x\tx\4")
        buf.write("y\ty\4z\tz\4{\t{\4|\t|\4}\t}\4~\t~\3\2\3\2\3\2\3\2\3\3")
        buf.write("\3\3\5\3\u0104\n\3\3\4\3\4\3\4\5\4\u0109\n\4\3\5\3\5\3")
        buf.write("\5\3\5\5\5\u010f\n\5\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3\r\3\r\3\r")
        buf.write("\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\20")
        buf.write("\3\20\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\22\3\22")
        buf.write("\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\23\3\24\3\24\3\24")
        buf.write("\3\25\3\25\3\25\3\25\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\27\3\27\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\30")
        buf.write("\3\30\3\30\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\32\3\32")
        buf.write("\3\32\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\35\3\35")
        buf.write("\3\35\3\36\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37")
        buf.write("\3 \3 \3 \3 \3 \3 \3!\3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3")
        buf.write("\"\3\"\3#\3#\3#\3#\3$\3$\3$\3$\3$\3%\3%\3%\3%\3%\3%\3")
        buf.write("%\3%\3%\3&\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3(\3")
        buf.write("(\3(\3(\3(\3(\3)\3)\3)\5)\u01d2\n)\3)\3)\5)\u01d6\n)\3")
        buf.write(")\5)\u01d9\n)\5)\u01db\n)\3)\3)\3*\3*\7*\u01e1\n*\f*\16")
        buf.write("*\u01e4\13*\3+\3+\3+\3+\3+\5+\u01eb\n+\3+\3+\5+\u01ef")
        buf.write("\n+\3,\3,\3,\3,\3,\5,\u01f6\n,\3,\3,\5,\u01fa\n,\3-\3")
        buf.write("-\7-\u01fe\n-\f-\16-\u0201\13-\3-\6-\u0204\n-\r-\16-\u0205")
        buf.write("\5-\u0208\n-\3.\3.\3.\6.\u020d\n.\r.\16.\u020e\3/\3/\3")
        buf.write("/\6/\u0214\n/\r/\16/\u0215\3\60\3\60\3\60\6\60\u021b\n")
        buf.write("\60\r\60\16\60\u021c\3\61\3\61\5\61\u0221\n\61\3\62\3")
        buf.write("\62\5\62\u0225\n\62\3\62\3\62\3\63\3\63\3\64\3\64\3\64")
        buf.write("\3\64\3\65\3\65\3\66\3\66\3\66\3\67\3\67\3\67\38\38\3")
        buf.write("9\39\3:\3:\3;\3;\3;\3<\3<\3=\3=\3=\3>\3>\3>\3?\3?\3@\3")
        buf.write("@\3A\3A\3B\3B\3B\3C\3C\3C\3D\3D\3E\3E\3F\3F\3G\3G\3H\3")
        buf.write("H\3H\3I\3I\3J\3J\3J\3K\3K\3K\3L\3L\3M\3M\3N\3N\3N\3O\3")
        buf.write("O\3O\3P\3P\3P\3Q\3Q\3Q\3R\3R\3R\3S\3S\3T\3T\3T\3U\3U\3")
        buf.write("U\3V\3V\3V\3W\3W\3W\3X\3X\3X\3Y\3Y\3Y\3Z\3Z\3Z\3[\3[\3")
        buf.write("[\3\\\3\\\3\\\3]\3]\3]\3^\3^\3^\3^\3_\3_\3_\3_\3`\3`\3")
        buf.write("`\3`\3a\3a\3a\3a\3b\3b\3b\5b\u02ad\nb\3b\3b\3c\3c\3d\3")
        buf.write("d\3d\7d\u02b6\nd\fd\16d\u02b9\13d\3d\3d\3d\3d\7d\u02bf")
        buf.write("\nd\fd\16d\u02c2\13d\3d\5d\u02c5\nd\3e\3e\3e\3e\3e\7e")
        buf.write("\u02cc\ne\fe\16e\u02cf\13e\3e\3e\3e\3e\3e\3e\3e\3e\7e")
        buf.write("\u02d9\ne\fe\16e\u02dc\13e\3e\3e\3e\5e\u02e1\ne\3f\3f")
        buf.write("\5f\u02e5\nf\3g\3g\3h\3h\3h\3h\5h\u02ed\nh\3i\3i\3j\3")
        buf.write("j\3k\3k\3l\3l\3m\3m\3n\5n\u02fa\nn\3n\3n\3n\3n\5n\u0300")
        buf.write("\nn\3o\3o\5o\u0304\no\3o\3o\3p\6p\u0309\np\rp\16p\u030a")
        buf.write("\3q\3q\6q\u030f\nq\rq\16q\u0310\3r\3r\5r\u0315\nr\3r\6")
        buf.write("r\u0318\nr\rr\16r\u0319\3s\3s\3s\7s\u031f\ns\fs\16s\u0322")
        buf.write("\13s\3s\3s\3s\3s\7s\u0328\ns\fs\16s\u032b\13s\3s\5s\u032e")
        buf.write("\ns\3t\3t\3t\3t\3t\7t\u0335\nt\ft\16t\u0338\13t\3t\3t")
        buf.write("\3t\3t\3t\3t\3t\3t\7t\u0342\nt\ft\16t\u0345\13t\3t\3t")
        buf.write("\3t\5t\u034a\nt\3u\3u\5u\u034e\nu\3v\5v\u0351\nv\3w\5")
        buf.write("w\u0354\nw\3x\5x\u0357\nx\3y\3y\3y\3z\6z\u035d\nz\rz\16")
        buf.write("z\u035e\3{\3{\7{\u0363\n{\f{\16{\u0366\13{\3|\3|\5|\u036a")
        buf.write("\n|\3|\5|\u036d\n|\3|\3|\5|\u0371\n|\3}\5}\u0374\n}\3")
        buf.write("~\3~\5~\u0378\n~\6\u02cd\u02da\u0336\u0343\2\177\3\3\5")
        buf.write("\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33")
        buf.write("\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32")
        buf.write("\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U")
        buf.write(",W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q:s;u<w=y>")
        buf.write("{?}@\177A\u0081B\u0083C\u0085D\u0087E\u0089F\u008bG\u008d")
        buf.write("H\u008fI\u0091J\u0093K\u0095L\u0097M\u0099N\u009bO\u009d")
        buf.write("P\u009fQ\u00a1R\u00a3S\u00a5T\u00a7U\u00a9V\u00abW\u00ad")
        buf.write("X\u00afY\u00b1Z\u00b3[\u00b5\\\u00b7]\u00b9^\u00bb_\u00bd")
        buf.write("`\u00bfa\u00c1b\u00c3c\u00c5d\u00c7\2\u00c9\2\u00cb\2")
        buf.write("\u00cd\2\u00cf\2\u00d1\2\u00d3\2\u00d5\2\u00d7\2\u00d9")
        buf.write("\2\u00db\2\u00dd\2\u00df\2\u00e1\2\u00e3\2\u00e5\2\u00e7")
        buf.write("\2\u00e9\2\u00eb\2\u00ed\2\u00ef\2\u00f1\2\u00f3\2\u00f5")
        buf.write("\2\u00f7\2\u00f9\2\u00fb\2\3\2\33\b\2HHTTWWhhttww\4\2")
        buf.write("HHhh\4\2TTtt\4\2DDdd\4\2QQqq\4\2ZZzz\4\2LLll\6\2\f\f\16")
        buf.write("\17))^^\6\2\f\f\16\17$$^^\3\2^^\3\2\63;\3\2\62;\3\2\62")
        buf.write("9\5\2\62;CHch\3\2\62\63\4\2GGgg\4\2--//\7\2\2\13\r\16")
        buf.write("\20(*]_\u0081\7\2\2\13\r\16\20#%]_\u0081\4\2\2]_\u0081")
        buf.write("\3\2\2\u0081\4\2\13\13\"\"\4\2\f\f\16\17\u0129\2C\\aa")
        buf.write("c|\u00ac\u00ac\u00b7\u00b7\u00bc\u00bc\u00c2\u00d8\u00da")
        buf.write("\u00f8\u00fa\u0243\u0252\u02c3\u02c8\u02d3\u02e2\u02e6")
        buf.write("\u02f0\u02f0\u037c\u037c\u0388\u0388\u038a\u038c\u038e")
        buf.write("\u038e\u0390\u03a3\u03a5\u03d0\u03d2\u03f7\u03f9\u0483")
        buf.write("\u048c\u04d0\u04d2\u04fb\u0502\u0511\u0533\u0558\u055b")
        buf.write("\u055b\u0563\u0589\u05d2\u05ec\u05f2\u05f4\u0623\u063c")
        buf.write("\u0642\u064c\u0670\u0671\u0673\u06d5\u06d7\u06d7\u06e7")
        buf.write("\u06e8\u06f0\u06f1\u06fc\u06fe\u0701\u0701\u0712\u0712")
        buf.write("\u0714\u0731\u074f\u076f\u0782\u07a7\u07b3\u07b3\u0906")
        buf.write("\u093b\u093f\u093f\u0952\u0952\u095a\u0963\u097f\u097f")
        buf.write("\u0987\u098e\u0991\u0992\u0995\u09aa\u09ac\u09b2\u09b4")
        buf.write("\u09b4\u09b8\u09bb\u09bf\u09bf\u09d0\u09d0\u09de\u09df")
        buf.write("\u09e1\u09e3\u09f2\u09f3\u0a07\u0a0c\u0a11\u0a12\u0a15")
        buf.write("\u0a2a\u0a2c\u0a32\u0a34\u0a35\u0a37\u0a38\u0a3a\u0a3b")
        buf.write("\u0a5b\u0a5e\u0a60\u0a60\u0a74\u0a76\u0a87\u0a8f\u0a91")
        buf.write("\u0a93\u0a95\u0aaa\u0aac\u0ab2\u0ab4\u0ab5\u0ab7\u0abb")
        buf.write("\u0abf\u0abf\u0ad2\u0ad2\u0ae2\u0ae3\u0b07\u0b0e\u0b11")
        buf.write("\u0b12\u0b15\u0b2a\u0b2c\u0b32\u0b34\u0b35\u0b37\u0b3b")
        buf.write("\u0b3f\u0b3f\u0b5e\u0b5f\u0b61\u0b63\u0b73\u0b73\u0b85")
        buf.write("\u0b85\u0b87\u0b8c\u0b90\u0b92\u0b94\u0b97\u0b9b\u0b9c")
        buf.write("\u0b9e\u0b9e\u0ba0\u0ba1\u0ba5\u0ba6\u0baa\u0bac\u0bb0")
        buf.write("\u0bbb\u0c07\u0c0e\u0c10\u0c12\u0c14\u0c2a\u0c2c\u0c35")
        buf.write("\u0c37\u0c3b\u0c62\u0c63\u0c87\u0c8e\u0c90\u0c92\u0c94")
        buf.write("\u0caa\u0cac\u0cb5\u0cb7\u0cbb\u0cbf\u0cbf\u0ce0\u0ce0")
        buf.write("\u0ce2\u0ce3\u0d07\u0d0e\u0d10\u0d12\u0d14\u0d2a\u0d2c")
        buf.write("\u0d3b\u0d62\u0d63\u0d87\u0d98\u0d9c\u0db3\u0db5\u0dbd")
        buf.write("\u0dbf\u0dbf\u0dc2\u0dc8\u0e03\u0e32\u0e34\u0e35\u0e42")
        buf.write("\u0e48\u0e83\u0e84\u0e86\u0e86\u0e89\u0e8a\u0e8c\u0e8c")
        buf.write("\u0e8f\u0e8f\u0e96\u0e99\u0e9b\u0ea1\u0ea3\u0ea5\u0ea7")
        buf.write("\u0ea7\u0ea9\u0ea9\u0eac\u0ead\u0eaf\u0eb2\u0eb4\u0eb5")
        buf.write("\u0ebf\u0ebf\u0ec2\u0ec6\u0ec8\u0ec8\u0ede\u0edf\u0f02")
        buf.write("\u0f02\u0f42\u0f49\u0f4b\u0f6c\u0f8a\u0f8d\u1002\u1023")
        buf.write("\u1025\u1029\u102b\u102c\u1052\u1057\u10a2\u10c7\u10d2")
        buf.write("\u10fc\u10fe\u10fe\u1102\u115b\u1161\u11a4\u11aa\u11fb")
        buf.write("\u1202\u124a\u124c\u124f\u1252\u1258\u125a\u125a\u125c")
        buf.write("\u125f\u1262\u128a\u128c\u128f\u1292\u12b2\u12b4\u12b7")
        buf.write("\u12ba\u12c0\u12c2\u12c2\u12c4\u12c7\u12ca\u12d8\u12da")
        buf.write("\u1312\u1314\u1317\u131a\u135c\u1382\u1391\u13a2\u13f6")
        buf.write("\u1403\u166e\u1671\u1678\u1683\u169c\u16a2\u16ec\u16f0")
        buf.write("\u16f2\u1702\u170e\u1710\u1713\u1722\u1733\u1742\u1753")
        buf.write("\u1762\u176e\u1770\u1772\u1782\u17b5\u17d9\u17d9\u17de")
        buf.write("\u17de\u1822\u1879\u1882\u18aa\u1902\u191e\u1952\u196f")
        buf.write("\u1972\u1976\u1982\u19ab\u19c3\u19c9\u1a02\u1a18\u1d02")
        buf.write("\u1dc1\u1e02\u1e9d\u1ea2\u1efb\u1f02\u1f17\u1f1a\u1f1f")
        buf.write("\u1f22\u1f47\u1f4a\u1f4f\u1f52\u1f59\u1f5b\u1f5b\u1f5d")
        buf.write("\u1f5d\u1f5f\u1f5f\u1f61\u1f7f\u1f82\u1fb6\u1fb8\u1fbe")
        buf.write("\u1fc0\u1fc0\u1fc4\u1fc6\u1fc8\u1fce\u1fd2\u1fd5\u1fd8")
        buf.write("\u1fdd\u1fe2\u1fee\u1ff4\u1ff6\u1ff8\u1ffe\u2073\u2073")
        buf.write("\u2081\u2081\u2092\u2096\u2104\u2104\u2109\u2109\u210c")
        buf.write("\u2115\u2117\u2117\u211a\u211f\u2126\u2126\u2128\u2128")
        buf.write("\u212a\u212a\u212c\u2133\u2135\u213b\u213e\u2141\u2147")
        buf.write("\u214b\u2162\u2185\u2c02\u2c30\u2c32\u2c60\u2c82\u2ce6")
        buf.write("\u2d02\u2d27\u2d32\u2d67\u2d71\u2d71\u2d82\u2d98\u2da2")
        buf.write("\u2da8\u2daa\u2db0\u2db2\u2db8\u2dba\u2dc0\u2dc2\u2dc8")
        buf.write("\u2dca\u2dd0\u2dd2\u2dd8\u2dda\u2de0\u3007\u3009\u3023")
        buf.write("\u302b\u3033\u3037\u303a\u303e\u3043\u3098\u309d\u30a1")
        buf.write("\u30a3\u30fc\u30fe\u3101\u3107\u312e\u3133\u3190\u31a2")
        buf.write("\u31b9\u31f2\u3201\u3402\u4db7\u4e02\u9fbd\ua002\ua48e")
        buf.write("\ua802\ua803\ua805\ua807\ua809\ua80c\ua80e\ua824\uac02")
        buf.write("\ud7a5\uf902\ufa2f\ufa32\ufa6c\ufa72\ufadb\ufb02\ufb08")
        buf.write("\ufb15\ufb19\ufb1f\ufb1f\ufb21\ufb2a\ufb2c\ufb38\ufb3a")
        buf.write("\ufb3e\ufb40\ufb40\ufb42\ufb43\ufb45\ufb46\ufb48\ufbb3")
        buf.write("\ufbd5\ufd3f\ufd52\ufd91\ufd94\ufdc9\ufdf2\ufdfd\ufe72")
        buf.write("\ufe76\ufe78\ufefe\uff23\uff3c\uff43\uff5c\uff68\uffc0")
        buf.write("\uffc4\uffc9\uffcc\uffd1\uffd4\uffd9\uffdc\uffde\u0096")
        buf.write("\2\62;\u0302\u0371\u0485\u0488\u0593\u05bb\u05bd\u05bf")
        buf.write("\u05c1\u05c1\u05c3\u05c4\u05c6\u05c7\u05c9\u05c9\u0612")
        buf.write("\u0617\u064d\u0660\u0662\u066b\u0672\u0672\u06d8\u06de")
        buf.write("\u06e1\u06e6\u06e9\u06ea\u06ec\u06ef\u06f2\u06fb\u0713")
        buf.write("\u0713\u0732\u074c\u07a8\u07b2\u0903\u0905\u093e\u093e")
        buf.write("\u0940\u094f\u0953\u0956\u0964\u0965\u0968\u0971\u0983")
        buf.write("\u0985\u09be\u09be\u09c0\u09c6\u09c9\u09ca\u09cd\u09cf")
        buf.write("\u09d9\u09d9\u09e4\u09e5\u09e8\u09f1\u0a03\u0a05\u0a3e")
        buf.write("\u0a3e\u0a40\u0a44\u0a49\u0a4a\u0a4d\u0a4f\u0a68\u0a73")
        buf.write("\u0a83\u0a85\u0abe\u0abe\u0ac0\u0ac7\u0ac9\u0acb\u0acd")
        buf.write("\u0acf\u0ae4\u0ae5\u0ae8\u0af1\u0b03\u0b05\u0b3e\u0b3e")
        buf.write("\u0b40\u0b45\u0b49\u0b4a\u0b4d\u0b4f\u0b58\u0b59\u0b68")
        buf.write("\u0b71\u0b84\u0b84\u0bc0\u0bc4\u0bc8\u0bca\u0bcc\u0bcf")
        buf.write("\u0bd9\u0bd9\u0be8\u0bf1\u0c03\u0c05\u0c40\u0c46\u0c48")
        buf.write("\u0c4a\u0c4c\u0c4f\u0c57\u0c58\u0c68\u0c71\u0c84\u0c85")
        buf.write("\u0cbe\u0cbe\u0cc0\u0cc6\u0cc8\u0cca\u0ccc\u0ccf\u0cd7")
        buf.write("\u0cd8\u0ce8\u0cf1\u0d04\u0d05\u0d40\u0d45\u0d48\u0d4a")
        buf.write("\u0d4c\u0d4f\u0d59\u0d59\u0d68\u0d71\u0d84\u0d85\u0dcc")
        buf.write("\u0dcc\u0dd1\u0dd6\u0dd8\u0dd8\u0dda\u0de1\u0df4\u0df5")
        buf.write("\u0e33\u0e33\u0e36\u0e3c\u0e49\u0e50\u0e52\u0e5b\u0eb3")
        buf.write("\u0eb3\u0eb6\u0ebb\u0ebd\u0ebe\u0eca\u0ecf\u0ed2\u0edb")
        buf.write("\u0f1a\u0f1b\u0f22\u0f2b\u0f37\u0f37\u0f39\u0f39\u0f3b")
        buf.write("\u0f3b\u0f40\u0f41\u0f73\u0f86\u0f88\u0f89\u0f92\u0f99")
        buf.write("\u0f9b\u0fbe\u0fc8\u0fc8\u102e\u1034\u1038\u103b\u1042")
        buf.write("\u104b\u1058\u105b\u1361\u1361\u136b\u1373\u1714\u1716")
        buf.write("\u1734\u1736\u1754\u1755\u1774\u1775\u17b8\u17d5\u17df")
        buf.write("\u17df\u17e2\u17eb\u180d\u180f\u1812\u181b\u18ab\u18ab")
        buf.write("\u1922\u192d\u1932\u193d\u1948\u1951\u19b2\u19c2\u19ca")
        buf.write("\u19cb\u19d2\u19db\u1a19\u1a1d\u1dc2\u1dc5\u2041\u2042")
        buf.write("\u2056\u2056\u20d2\u20de\u20e3\u20e3\u20e7\u20ed\u302c")
        buf.write("\u3031\u309b\u309c\ua804\ua804\ua808\ua808\ua80d\ua80d")
        buf.write("\ua825\ua829\ufb20\ufb20\ufe02\ufe11\ufe22\ufe25\ufe35")
        buf.write("\ufe36\ufe4f\ufe51\uff12\uff1b\uff41\uff41\2\u0399\2\3")
        buf.write("\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2")
        buf.write("\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2")
        buf.write("\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2")
        buf.write("\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3")
        buf.write("\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2")
        buf.write("/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67")
        buf.write("\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2")
        buf.write("A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2")
        buf.write("\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2")
        buf.write("\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2")
        buf.write("\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3")
        buf.write("\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q")
        buf.write("\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2")
        buf.write("{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083")
        buf.write("\3\2\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2")
        buf.write("\2\2\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f\3\2\2\2\2\u0091")
        buf.write("\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2\2\2\u0097\3\2\2")
        buf.write("\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d\3\2\2\2\2\u009f")
        buf.write("\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2\2\2\u00a5\3\2\2")
        buf.write("\2\2\u00a7\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab\3\2\2\2\2\u00ad")
        buf.write("\3\2\2\2\2\u00af\3\2\2\2\2\u00b1\3\2\2\2\2\u00b3\3\2\2")
        buf.write("\2\2\u00b5\3\2\2\2\2\u00b7\3\2\2\2\2\u00b9\3\2\2\2\2\u00bb")
        buf.write("\3\2\2\2\2\u00bd\3\2\2\2\2\u00bf\3\2\2\2\2\u00c1\3\2\2")
        buf.write("\2\2\u00c3\3\2\2\2\2\u00c5\3\2\2\2\3\u00fd\3\2\2\2\5\u0103")
        buf.write("\3\2\2\2\7\u0108\3\2\2\2\t\u010e\3\2\2\2\13\u0110\3\2")
        buf.write("\2\2\r\u0114\3\2\2\2\17\u011b\3\2\2\2\21\u0121\3\2\2\2")
        buf.write("\23\u0126\3\2\2\2\25\u012d\3\2\2\2\27\u0130\3\2\2\2\31")
        buf.write("\u0137\3\2\2\2\33\u0140\3\2\2\2\35\u0147\3\2\2\2\37\u014a")
        buf.write("\3\2\2\2!\u014f\3\2\2\2#\u0154\3\2\2\2%\u015a\3\2\2\2")
        buf.write("\'\u015e\3\2\2\2)\u0161\3\2\2\2+\u0165\3\2\2\2-\u016d")
        buf.write("\3\2\2\2/\u0172\3\2\2\2\61\u0179\3\2\2\2\63\u0180\3\2")
        buf.write("\2\2\65\u0183\3\2\2\2\67\u0187\3\2\2\29\u018b\3\2\2\2")
        buf.write(";\u018e\3\2\2\2=\u0193\3\2\2\2?\u0198\3\2\2\2A\u019e\3")
        buf.write("\2\2\2C\u01a4\3\2\2\2E\u01aa\3\2\2\2G\u01ae\3\2\2\2I\u01b3")
        buf.write("\3\2\2\2K\u01bc\3\2\2\2M\u01c2\3\2\2\2O\u01c8\3\2\2\2")
        buf.write("Q\u01da\3\2\2\2S\u01de\3\2\2\2U\u01ea\3\2\2\2W\u01f5\3")
        buf.write("\2\2\2Y\u0207\3\2\2\2[\u0209\3\2\2\2]\u0210\3\2\2\2_\u0217")
        buf.write("\3\2\2\2a\u0220\3\2\2\2c\u0224\3\2\2\2e\u0228\3\2\2\2")
        buf.write("g\u022a\3\2\2\2i\u022e\3\2\2\2k\u0230\3\2\2\2m\u0233\3")
        buf.write("\2\2\2o\u0236\3\2\2\2q\u0238\3\2\2\2s\u023a\3\2\2\2u\u023c")
        buf.write("\3\2\2\2w\u023f\3\2\2\2y\u0241\3\2\2\2{\u0244\3\2\2\2")
        buf.write("}\u0247\3\2\2\2\177\u0249\3\2\2\2\u0081\u024b\3\2\2\2")
        buf.write("\u0083\u024d\3\2\2\2\u0085\u0250\3\2\2\2\u0087\u0253\3")
        buf.write("\2\2\2\u0089\u0255\3\2\2\2\u008b\u0257\3\2\2\2\u008d\u0259")
        buf.write("\3\2\2\2\u008f\u025b\3\2\2\2\u0091\u025e\3\2\2\2\u0093")
        buf.write("\u0260\3\2\2\2\u0095\u0263\3\2\2\2\u0097\u0266\3\2\2\2")
        buf.write("\u0099\u0268\3\2\2\2\u009b\u026a\3\2\2\2\u009d\u026d\3")
        buf.write("\2\2\2\u009f\u0270\3\2\2\2\u00a1\u0273\3\2\2\2\u00a3\u0276")
        buf.write("\3\2\2\2\u00a5\u0279\3\2\2\2\u00a7\u027b\3\2\2\2\u00a9")
        buf.write("\u027e\3\2\2\2\u00ab\u0281\3\2\2\2\u00ad\u0284\3\2\2\2")
        buf.write("\u00af\u0287\3\2\2\2\u00b1\u028a\3\2\2\2\u00b3\u028d\3")
        buf.write("\2\2\2\u00b5\u0290\3\2\2\2\u00b7\u0293\3\2\2\2\u00b9\u0296")
        buf.write("\3\2\2\2\u00bb\u0299\3\2\2\2\u00bd\u029d\3\2\2\2\u00bf")
        buf.write("\u02a1\3\2\2\2\u00c1\u02a5\3\2\2\2\u00c3\u02ac\3\2\2\2")
        buf.write("\u00c5\u02b0\3\2\2\2\u00c7\u02c4\3\2\2\2\u00c9\u02e0\3")
        buf.write("\2\2\2\u00cb\u02e4\3\2\2\2\u00cd\u02e6\3\2\2\2\u00cf\u02ec")
        buf.write("\3\2\2\2\u00d1\u02ee\3\2\2\2\u00d3\u02f0\3\2\2\2\u00d5")
        buf.write("\u02f2\3\2\2\2\u00d7\u02f4\3\2\2\2\u00d9\u02f6\3\2\2\2")
        buf.write("\u00db\u02ff\3\2\2\2\u00dd\u0303\3\2\2\2\u00df\u0308\3")
        buf.write("\2\2\2\u00e1\u030c\3\2\2\2\u00e3\u0312\3\2\2\2\u00e5\u032d")
        buf.write("\3\2\2\2\u00e7\u0349\3\2\2\2\u00e9\u034d\3\2\2\2\u00eb")
        buf.write("\u0350\3\2\2\2\u00ed\u0353\3\2\2\2\u00ef\u0356\3\2\2\2")
        buf.write("\u00f1\u0358\3\2\2\2\u00f3\u035c\3\2\2\2\u00f5\u0360\3")
        buf.write("\2\2\2\u00f7\u0367\3\2\2\2\u00f9\u0373\3\2\2\2\u00fb\u0377")
        buf.write("\3\2\2\2\u00fd\u00fe\7k\2\2\u00fe\u00ff\7u\2\2\u00ff\u0100")
        buf.write("\7c\2\2\u0100\4\3\2\2\2\u0101\u0104\5U+\2\u0102\u0104")
        buf.write("\5W,\2\u0103\u0101\3\2\2\2\u0103\u0102\3\2\2\2\u0104\6")
        buf.write("\3\2\2\2\u0105\u0109\5\t\5\2\u0106\u0109\5a\61\2\u0107")
        buf.write("\u0109\5c\62\2\u0108\u0105\3\2\2\2\u0108\u0106\3\2\2\2")
        buf.write("\u0108\u0107\3\2\2\2\u0109\b\3\2\2\2\u010a\u010f\5Y-\2")
        buf.write("\u010b\u010f\5[.\2\u010c\u010f\5]/\2\u010d\u010f\5_\60")
        buf.write("\2\u010e\u010a\3\2\2\2\u010e\u010b\3\2\2\2\u010e\u010c")
        buf.write("\3\2\2\2\u010e\u010d\3\2\2\2\u010f\n\3\2\2\2\u0110\u0111")
        buf.write("\7f\2\2\u0111\u0112\7g\2\2\u0112\u0113\7h\2\2\u0113\f")
        buf.write("\3\2\2\2\u0114\u0115\7t\2\2\u0115\u0116\7g\2\2\u0116\u0117")
        buf.write("\7v\2\2\u0117\u0118\7w\2\2\u0118\u0119\7t\2\2\u0119\u011a")
        buf.write("\7p\2\2\u011a\16\3\2\2\2\u011b\u011c\7t\2\2\u011c\u011d")
        buf.write("\7c\2\2\u011d\u011e\7k\2\2\u011e\u011f\7u\2\2\u011f\u0120")
        buf.write("\7g\2\2\u0120\20\3\2\2\2\u0121\u0122\7h\2\2\u0122\u0123")
        buf.write("\7t\2\2\u0123\u0124\7q\2\2\u0124\u0125\7o\2\2\u0125\22")
        buf.write("\3\2\2\2\u0126\u0127\7k\2\2\u0127\u0128\7o\2\2\u0128\u0129")
        buf.write("\7r\2\2\u0129\u012a\7q\2\2\u012a\u012b\7t\2\2\u012b\u012c")
        buf.write("\7v\2\2\u012c\24\3\2\2\2\u012d\u012e\7c\2\2\u012e\u012f")
        buf.write("\7u\2\2\u012f\26\3\2\2\2\u0130\u0131\7i\2\2\u0131\u0132")
        buf.write("\7n\2\2\u0132\u0133\7q\2\2\u0133\u0134\7d\2\2\u0134\u0135")
        buf.write("\7c\2\2\u0135\u0136\7n\2\2\u0136\30\3\2\2\2\u0137\u0138")
        buf.write("\7p\2\2\u0138\u0139\7q\2\2\u0139\u013a\7p\2\2\u013a\u013b")
        buf.write("\7n\2\2\u013b\u013c\7q\2\2\u013c\u013d\7e\2\2\u013d\u013e")
        buf.write("\7c\2\2\u013e\u013f\7n\2\2\u013f\32\3\2\2\2\u0140\u0141")
        buf.write("\7c\2\2\u0141\u0142\7u\2\2\u0142\u0143\7u\2\2\u0143\u0144")
        buf.write("\7g\2\2\u0144\u0145\7t\2\2\u0145\u0146\7v\2\2\u0146\34")
        buf.write("\3\2\2\2\u0147\u0148\7k\2\2\u0148\u0149\7h\2\2\u0149\36")
        buf.write("\3\2\2\2\u014a\u014b\7g\2\2\u014b\u014c\7n\2\2\u014c\u014d")
        buf.write("\7k\2\2\u014d\u014e\7h\2\2\u014e \3\2\2\2\u014f\u0150")
        buf.write("\7g\2\2\u0150\u0151\7n\2\2\u0151\u0152\7u\2\2\u0152\u0153")
        buf.write("\7g\2\2\u0153\"\3\2\2\2\u0154\u0155\7y\2\2\u0155\u0156")
        buf.write("\7j\2\2\u0156\u0157\7k\2\2\u0157\u0158\7n\2\2\u0158\u0159")
        buf.write("\7g\2\2\u0159$\3\2\2\2\u015a\u015b\7h\2\2\u015b\u015c")
        buf.write("\7q\2\2\u015c\u015d\7t\2\2\u015d&\3\2\2\2\u015e\u015f")
        buf.write("\7k\2\2\u015f\u0160\7p\2\2\u0160(\3\2\2\2\u0161\u0162")
        buf.write("\7v\2\2\u0162\u0163\7t\2\2\u0163\u0164\7{\2\2\u0164*\3")
        buf.write("\2\2\2\u0165\u0166\7h\2\2\u0166\u0167\7k\2\2\u0167\u0168")
        buf.write("\7p\2\2\u0168\u0169\7c\2\2\u0169\u016a\7n\2\2\u016a\u016b")
        buf.write("\7n\2\2\u016b\u016c\7{\2\2\u016c,\3\2\2\2\u016d\u016e")
        buf.write("\7y\2\2\u016e\u016f\7k\2\2\u016f\u0170\7v\2\2\u0170\u0171")
        buf.write("\7j\2\2\u0171.\3\2\2\2\u0172\u0173\7g\2\2\u0173\u0174")
        buf.write("\7z\2\2\u0174\u0175\7e\2\2\u0175\u0176\7g\2\2\u0176\u0177")
        buf.write("\7r\2\2\u0177\u0178\7v\2\2\u0178\60\3\2\2\2\u0179\u017a")
        buf.write("\7n\2\2\u017a\u017b\7c\2\2\u017b\u017c\7o\2\2\u017c\u017d")
        buf.write("\7d\2\2\u017d\u017e\7f\2\2\u017e\u017f\7c\2\2\u017f\62")
        buf.write("\3\2\2\2\u0180\u0181\7q\2\2\u0181\u0182\7t\2\2\u0182\64")
        buf.write("\3\2\2\2\u0183\u0184\7c\2\2\u0184\u0185\7p\2\2\u0185\u0186")
        buf.write("\7f\2\2\u0186\66\3\2\2\2\u0187\u0188\7p\2\2\u0188\u0189")
        buf.write("\7q\2\2\u0189\u018a\7v\2\2\u018a8\3\2\2\2\u018b\u018c")
        buf.write("\7k\2\2\u018c\u018d\7u\2\2\u018d:\3\2\2\2\u018e\u018f")
        buf.write("\7p\2\2\u018f\u0190\7q\2\2\u0190\u0191\7p\2\2\u0191\u0192")
        buf.write("\7g\2\2\u0192<\3\2\2\2\u0193\u0194\7v\2\2\u0194\u0195")
        buf.write("\7t\2\2\u0195\u0196\7w\2\2\u0196\u0197\7g\2\2\u0197>\3")
        buf.write("\2\2\2\u0198\u0199\7h\2\2\u0199\u019a\7c\2\2\u019a\u019b")
        buf.write("\7n\2\2\u019b\u019c\7u\2\2\u019c\u019d\7g\2\2\u019d@\3")
        buf.write("\2\2\2\u019e\u019f\7e\2\2\u019f\u01a0\7n\2\2\u01a0\u01a1")
        buf.write("\7c\2\2\u01a1\u01a2\7u\2\2\u01a2\u01a3\7u\2\2\u01a3B\3")
        buf.write("\2\2\2\u01a4\u01a5\7{\2\2\u01a5\u01a6\7k\2\2\u01a6\u01a7")
        buf.write("\7g\2\2\u01a7\u01a8\7n\2\2\u01a8\u01a9\7f\2\2\u01a9D\3")
        buf.write("\2\2\2\u01aa\u01ab\7f\2\2\u01ab\u01ac\7g\2\2\u01ac\u01ad")
        buf.write("\7n\2\2\u01adF\3\2\2\2\u01ae\u01af\7r\2\2\u01af\u01b0")
        buf.write("\7c\2\2\u01b0\u01b1\7u\2\2\u01b1\u01b2\7u\2\2\u01b2H\3")
        buf.write("\2\2\2\u01b3\u01b4\7e\2\2\u01b4\u01b5\7q\2\2\u01b5\u01b6")
        buf.write("\7p\2\2\u01b6\u01b7\7v\2\2\u01b7\u01b8\7k\2\2\u01b8\u01b9")
        buf.write("\7p\2\2\u01b9\u01ba\7w\2\2\u01ba\u01bb\7g\2\2\u01bbJ\3")
        buf.write("\2\2\2\u01bc\u01bd\7d\2\2\u01bd\u01be\7t\2\2\u01be\u01bf")
        buf.write("\7g\2\2\u01bf\u01c0\7c\2\2\u01c0\u01c1\7m\2\2\u01c1L\3")
        buf.write("\2\2\2\u01c2\u01c3\7c\2\2\u01c3\u01c4\7u\2\2\u01c4\u01c5")
        buf.write("\7{\2\2\u01c5\u01c6\7p\2\2\u01c6\u01c7\7e\2\2\u01c7N\3")
        buf.write("\2\2\2\u01c8\u01c9\7c\2\2\u01c9\u01ca\7y\2\2\u01ca\u01cb")
        buf.write("\7c\2\2\u01cb\u01cc\7k\2\2\u01cc\u01cd\7v\2\2\u01cdP\3")
        buf.write("\2\2\2\u01ce\u01cf\6)\2\2\u01cf\u01db\5\u00f3z\2\u01d0")
        buf.write("\u01d2\7\17\2\2\u01d1\u01d0\3\2\2\2\u01d1\u01d2\3\2\2")
        buf.write("\2\u01d2\u01d3\3\2\2\2\u01d3\u01d6\7\f\2\2\u01d4\u01d6")
        buf.write("\4\16\17\2\u01d5\u01d1\3\2\2\2\u01d5\u01d4\3\2\2\2\u01d6")
        buf.write("\u01d8\3\2\2\2\u01d7\u01d9\5\u00f3z\2\u01d8\u01d7\3\2")
        buf.write("\2\2\u01d8\u01d9\3\2\2\2\u01d9\u01db\3\2\2\2\u01da\u01ce")
        buf.write("\3\2\2\2\u01da\u01d5\3\2\2\2\u01db\u01dc\3\2\2\2\u01dc")
        buf.write("\u01dd\b)\2\2\u01ddR\3\2\2\2\u01de\u01e2\5\u00f9}\2\u01df")
        buf.write("\u01e1\5\u00fb~\2\u01e0\u01df\3\2\2\2\u01e1\u01e4\3\2")
        buf.write("\2\2\u01e2\u01e0\3\2\2\2\u01e2\u01e3\3\2\2\2\u01e3T\3")
        buf.write("\2\2\2\u01e4\u01e2\3\2\2\2\u01e5\u01eb\t\2\2\2\u01e6\u01e7")
        buf.write("\t\3\2\2\u01e7\u01eb\t\4\2\2\u01e8\u01e9\t\4\2\2\u01e9")
        buf.write("\u01eb\t\3\2\2\u01ea\u01e5\3\2\2\2\u01ea\u01e6\3\2\2\2")
        buf.write("\u01ea\u01e8\3\2\2\2\u01ea\u01eb\3\2\2\2\u01eb\u01ee\3")
        buf.write("\2\2\2\u01ec\u01ef\5\u00c7d\2\u01ed\u01ef\5\u00c9e\2\u01ee")
        buf.write("\u01ec\3\2\2\2\u01ee\u01ed\3\2\2\2\u01efV\3\2\2\2\u01f0")
        buf.write("\u01f6\t\5\2\2\u01f1\u01f2\t\5\2\2\u01f2\u01f6\t\4\2\2")
        buf.write("\u01f3\u01f4\t\4\2\2\u01f4\u01f6\t\5\2\2\u01f5\u01f0\3")
        buf.write("\2\2\2\u01f5\u01f1\3\2\2\2\u01f5\u01f3\3\2\2\2\u01f6\u01f9")
        buf.write("\3\2\2\2\u01f7\u01fa\5\u00e5s\2\u01f8\u01fa\5\u00e7t\2")
        buf.write("\u01f9\u01f7\3\2\2\2\u01f9\u01f8\3\2\2\2\u01faX\3\2\2")
        buf.write("\2\u01fb\u01ff\5\u00d1i\2\u01fc\u01fe\5\u00d3j\2\u01fd")
        buf.write("\u01fc\3\2\2\2\u01fe\u0201\3\2\2\2\u01ff\u01fd\3\2\2\2")
        buf.write("\u01ff\u0200\3\2\2\2\u0200\u0208\3\2\2\2\u0201\u01ff\3")
        buf.write("\2\2\2\u0202\u0204\7\62\2\2\u0203\u0202\3\2\2\2\u0204")
        buf.write("\u0205\3\2\2\2\u0205\u0203\3\2\2\2\u0205\u0206\3\2\2\2")
        buf.write("\u0206\u0208\3\2\2\2\u0207\u01fb\3\2\2\2\u0207\u0203\3")
        buf.write("\2\2\2\u0208Z\3\2\2\2\u0209\u020a\7\62\2\2\u020a\u020c")
        buf.write("\t\6\2\2\u020b\u020d\5\u00d5k\2\u020c\u020b\3\2\2\2\u020d")
        buf.write("\u020e\3\2\2\2\u020e\u020c\3\2\2\2\u020e\u020f\3\2\2\2")
        buf.write("\u020f\\\3\2\2\2\u0210\u0211\7\62\2\2\u0211\u0213\t\7")
        buf.write("\2\2\u0212\u0214\5\u00d7l\2\u0213\u0212\3\2\2\2\u0214")
        buf.write("\u0215\3\2\2\2\u0215\u0213\3\2\2\2\u0215\u0216\3\2\2\2")
        buf.write("\u0216^\3\2\2\2\u0217\u0218\7\62\2\2\u0218\u021a\t\5\2")
        buf.write("\2\u0219\u021b\5\u00d9m\2\u021a\u0219\3\2\2\2\u021b\u021c")
        buf.write("\3\2\2\2\u021c\u021a\3\2\2\2\u021c\u021d\3\2\2\2\u021d")
        buf.write("`\3\2\2\2\u021e\u0221\5\u00dbn\2\u021f\u0221\5\u00ddo")
        buf.write("\2\u0220\u021e\3\2\2\2\u0220\u021f\3\2\2\2\u0221b\3\2")
        buf.write("\2\2\u0222\u0225\5a\61\2\u0223\u0225\5\u00dfp\2\u0224")
        buf.write("\u0222\3\2\2\2\u0224\u0223\3\2\2\2\u0225\u0226\3\2\2\2")
        buf.write("\u0226\u0227\t\b\2\2\u0227d\3\2\2\2\u0228\u0229\7\60\2")
        buf.write("\2\u0229f\3\2\2\2\u022a\u022b\7\60\2\2\u022b\u022c\7\60")
        buf.write("\2\2\u022c\u022d\7\60\2\2\u022dh\3\2\2\2\u022e\u022f\7")
        buf.write(",\2\2\u022fj\3\2\2\2\u0230\u0231\7*\2\2\u0231\u0232\b")
        buf.write("\66\3\2\u0232l\3\2\2\2\u0233\u0234\7+\2\2\u0234\u0235")
        buf.write("\b\67\4\2\u0235n\3\2\2\2\u0236\u0237\7.\2\2\u0237p\3\2")
        buf.write("\2\2\u0238\u0239\7<\2\2\u0239r\3\2\2\2\u023a\u023b\7=")
        buf.write("\2\2\u023bt\3\2\2\2\u023c\u023d\7,\2\2\u023d\u023e\7,")
        buf.write("\2\2\u023ev\3\2\2\2\u023f\u0240\7?\2\2\u0240x\3\2\2\2")
        buf.write("\u0241\u0242\7]\2\2\u0242\u0243\b=\5\2\u0243z\3\2\2\2")
        buf.write("\u0244\u0245\7_\2\2\u0245\u0246\b>\6\2\u0246|\3\2\2\2")
        buf.write("\u0247\u0248\7~\2\2\u0248~\3\2\2\2\u0249\u024a\7`\2\2")
        buf.write("\u024a\u0080\3\2\2\2\u024b\u024c\7(\2\2\u024c\u0082\3")
        buf.write("\2\2\2\u024d\u024e\7>\2\2\u024e\u024f\7>\2\2\u024f\u0084")
        buf.write("\3\2\2\2\u0250\u0251\7@\2\2\u0251\u0252\7@\2\2\u0252\u0086")
        buf.write("\3\2\2\2\u0253\u0254\7-\2\2\u0254\u0088\3\2\2\2\u0255")
        buf.write("\u0256\7/\2\2\u0256\u008a\3\2\2\2\u0257\u0258\7\61\2\2")
        buf.write("\u0258\u008c\3\2\2\2\u0259\u025a\7\'\2\2\u025a\u008e\3")
        buf.write("\2\2\2\u025b\u025c\7\61\2\2\u025c\u025d\7\61\2\2\u025d")
        buf.write("\u0090\3\2\2\2\u025e\u025f\7\u0080\2\2\u025f\u0092\3\2")
        buf.write("\2\2\u0260\u0261\7}\2\2\u0261\u0262\bJ\7\2\u0262\u0094")
        buf.write("\3\2\2\2\u0263\u0264\7\177\2\2\u0264\u0265\bK\b\2\u0265")
        buf.write("\u0096\3\2\2\2\u0266\u0267\7>\2\2\u0267\u0098\3\2\2\2")
        buf.write("\u0268\u0269\7@\2\2\u0269\u009a\3\2\2\2\u026a\u026b\7")
        buf.write("?\2\2\u026b\u026c\7?\2\2\u026c\u009c\3\2\2\2\u026d\u026e")
        buf.write("\7@\2\2\u026e\u026f\7?\2\2\u026f\u009e\3\2\2\2\u0270\u0271")
        buf.write("\7>\2\2\u0271\u0272\7?\2\2\u0272\u00a0\3\2\2\2\u0273\u0274")
        buf.write("\7>\2\2\u0274\u0275\7@\2\2\u0275\u00a2\3\2\2\2\u0276\u0277")
        buf.write("\7#\2\2\u0277\u0278\7?\2\2\u0278\u00a4\3\2\2\2\u0279\u027a")
        buf.write("\7B\2\2\u027a\u00a6\3\2\2\2\u027b\u027c\7/\2\2\u027c\u027d")
        buf.write("\7@\2\2\u027d\u00a8\3\2\2\2\u027e\u027f\7-\2\2\u027f\u0280")
        buf.write("\7?\2\2\u0280\u00aa\3\2\2\2\u0281\u0282\7/\2\2\u0282\u0283")
        buf.write("\7?\2\2\u0283\u00ac\3\2\2\2\u0284\u0285\7,\2\2\u0285\u0286")
        buf.write("\7?\2\2\u0286\u00ae\3\2\2\2\u0287\u0288\7B\2\2\u0288\u0289")
        buf.write("\7?\2\2\u0289\u00b0\3\2\2\2\u028a\u028b\7\61\2\2\u028b")
        buf.write("\u028c\7?\2\2\u028c\u00b2\3\2\2\2\u028d\u028e\7\'\2\2")
        buf.write("\u028e\u028f\7?\2\2\u028f\u00b4\3\2\2\2\u0290\u0291\7")
        buf.write("(\2\2\u0291\u0292\7?\2\2\u0292\u00b6\3\2\2\2\u0293\u0294")
        buf.write("\7~\2\2\u0294\u0295\7?\2\2\u0295\u00b8\3\2\2\2\u0296\u0297")
        buf.write("\7`\2\2\u0297\u0298\7?\2\2\u0298\u00ba\3\2\2\2\u0299\u029a")
        buf.write("\7>\2\2\u029a\u029b\7>\2\2\u029b\u029c\7?\2\2\u029c\u00bc")
        buf.write("\3\2\2\2\u029d\u029e\7@\2\2\u029e\u029f\7@\2\2\u029f\u02a0")
        buf.write("\7?\2\2\u02a0\u00be\3\2\2\2\u02a1\u02a2\7,\2\2\u02a2\u02a3")
        buf.write("\7,\2\2\u02a3\u02a4\7?\2\2\u02a4\u00c0\3\2\2\2\u02a5\u02a6")
        buf.write("\7\61\2\2\u02a6\u02a7\7\61\2\2\u02a7\u02a8\7?\2\2\u02a8")
        buf.write("\u00c2\3\2\2\2\u02a9\u02ad\5\u00f3z\2\u02aa\u02ad\5\u00f5")
        buf.write("{\2\u02ab\u02ad\5\u00f7|\2\u02ac\u02a9\3\2\2\2\u02ac\u02aa")
        buf.write("\3\2\2\2\u02ac\u02ab\3\2\2\2\u02ad\u02ae\3\2\2\2\u02ae")
        buf.write("\u02af\bb\t\2\u02af\u00c4\3\2\2\2\u02b0\u02b1\13\2\2\2")
        buf.write("\u02b1\u00c6\3\2\2\2\u02b2\u02b7\7)\2\2\u02b3\u02b6\5")
        buf.write("\u00cfh\2\u02b4\u02b6\n\t\2\2\u02b5\u02b3\3\2\2\2\u02b5")
        buf.write("\u02b4\3\2\2\2\u02b6\u02b9\3\2\2\2\u02b7\u02b5\3\2\2\2")
        buf.write("\u02b7\u02b8\3\2\2\2\u02b8\u02ba\3\2\2\2\u02b9\u02b7\3")
        buf.write("\2\2\2\u02ba\u02c5\7)\2\2\u02bb\u02c0\7$\2\2\u02bc\u02bf")
        buf.write("\5\u00cfh\2\u02bd\u02bf\n\n\2\2\u02be\u02bc\3\2\2\2\u02be")
        buf.write("\u02bd\3\2\2\2\u02bf\u02c2\3\2\2\2\u02c0\u02be\3\2\2\2")
        buf.write("\u02c0\u02c1\3\2\2\2\u02c1\u02c3\3\2\2\2\u02c2\u02c0\3")
        buf.write("\2\2\2\u02c3\u02c5\7$\2\2\u02c4\u02b2\3\2\2\2\u02c4\u02bb")
        buf.write("\3\2\2\2\u02c5\u00c8\3\2\2\2\u02c6\u02c7\7)\2\2\u02c7")
        buf.write("\u02c8\7)\2\2\u02c8\u02c9\7)\2\2\u02c9\u02cd\3\2\2\2\u02ca")
        buf.write("\u02cc\5\u00cbf\2\u02cb\u02ca\3\2\2\2\u02cc\u02cf\3\2")
        buf.write("\2\2\u02cd\u02ce\3\2\2\2\u02cd\u02cb\3\2\2\2\u02ce\u02d0")
        buf.write("\3\2\2\2\u02cf\u02cd\3\2\2\2\u02d0\u02d1\7)\2\2\u02d1")
        buf.write("\u02d2\7)\2\2\u02d2\u02e1\7)\2\2\u02d3\u02d4\7$\2\2\u02d4")
        buf.write("\u02d5\7$\2\2\u02d5\u02d6\7$\2\2\u02d6\u02da\3\2\2\2\u02d7")
        buf.write("\u02d9\5\u00cbf\2\u02d8\u02d7\3\2\2\2\u02d9\u02dc\3\2")
        buf.write("\2\2\u02da\u02db\3\2\2\2\u02da\u02d8\3\2\2\2\u02db\u02dd")
        buf.write("\3\2\2\2\u02dc\u02da\3\2\2\2\u02dd\u02de\7$\2\2\u02de")
        buf.write("\u02df\7$\2\2\u02df\u02e1\7$\2\2\u02e0\u02c6\3\2\2\2\u02e0")
        buf.write("\u02d3\3\2\2\2\u02e1\u00ca\3\2\2\2\u02e2\u02e5\5\u00cd")
        buf.write("g\2\u02e3\u02e5\5\u00cfh\2\u02e4\u02e2\3\2\2\2\u02e4\u02e3")
        buf.write("\3\2\2\2\u02e5\u00cc\3\2\2\2\u02e6\u02e7\n\13\2\2\u02e7")
        buf.write("\u00ce\3\2\2\2\u02e8\u02e9\7^\2\2\u02e9\u02ed\13\2\2\2")
        buf.write("\u02ea\u02eb\7^\2\2\u02eb\u02ed\5Q)\2\u02ec\u02e8\3\2")
        buf.write("\2\2\u02ec\u02ea\3\2\2\2\u02ed\u00d0\3\2\2\2\u02ee\u02ef")
        buf.write("\t\f\2\2\u02ef\u00d2\3\2\2\2\u02f0\u02f1\t\r\2\2\u02f1")
        buf.write("\u00d4\3\2\2\2\u02f2\u02f3\t\16\2\2\u02f3\u00d6\3\2\2")
        buf.write("\2\u02f4\u02f5\t\17\2\2\u02f5\u00d8\3\2\2\2\u02f6\u02f7")
        buf.write("\t\20\2\2\u02f7\u00da\3\2\2\2\u02f8\u02fa\5\u00dfp\2\u02f9")
        buf.write("\u02f8\3\2\2\2\u02f9\u02fa\3\2\2\2\u02fa\u02fb\3\2\2\2")
        buf.write("\u02fb\u0300\5\u00e1q\2\u02fc\u02fd\5\u00dfp\2\u02fd\u02fe")
        buf.write("\7\60\2\2\u02fe\u0300\3\2\2\2\u02ff\u02f9\3\2\2\2\u02ff")
        buf.write("\u02fc\3\2\2\2\u0300\u00dc\3\2\2\2\u0301\u0304\5\u00df")
        buf.write("p\2\u0302\u0304\5\u00dbn\2\u0303\u0301\3\2\2\2\u0303\u0302")
        buf.write("\3\2\2\2\u0304\u0305\3\2\2\2\u0305\u0306\5\u00e3r\2\u0306")
        buf.write("\u00de\3\2\2\2\u0307\u0309\5\u00d3j\2\u0308\u0307\3\2")
        buf.write("\2\2\u0309\u030a\3\2\2\2\u030a\u0308\3\2\2\2\u030a\u030b")
        buf.write("\3\2\2\2\u030b\u00e0\3\2\2\2\u030c\u030e\7\60\2\2\u030d")
        buf.write("\u030f\5\u00d3j\2\u030e\u030d\3\2\2\2\u030f\u0310\3\2")
        buf.write("\2\2\u0310\u030e\3\2\2\2\u0310\u0311\3\2\2\2\u0311\u00e2")
        buf.write("\3\2\2\2\u0312\u0314\t\21\2\2\u0313\u0315\t\22\2\2\u0314")
        buf.write("\u0313\3\2\2\2\u0314\u0315\3\2\2\2\u0315\u0317\3\2\2\2")
        buf.write("\u0316\u0318\5\u00d3j\2\u0317\u0316\3\2\2\2\u0318\u0319")
        buf.write("\3\2\2\2\u0319\u0317\3\2\2\2\u0319\u031a\3\2\2\2\u031a")
        buf.write("\u00e4\3\2\2\2\u031b\u0320\7)\2\2\u031c\u031f\5\u00eb")
        buf.write("v\2\u031d\u031f\5\u00f1y\2\u031e\u031c\3\2\2\2\u031e\u031d")
        buf.write("\3\2\2\2\u031f\u0322\3\2\2\2\u0320\u031e\3\2\2\2\u0320")
        buf.write("\u0321\3\2\2\2\u0321\u0323\3\2\2\2\u0322\u0320\3\2\2\2")
        buf.write("\u0323\u032e\7)\2\2\u0324\u0329\7$\2\2\u0325\u0328\5\u00ed")
        buf.write("w\2\u0326\u0328\5\u00f1y\2\u0327\u0325\3\2\2\2\u0327\u0326")
        buf.write("\3\2\2\2\u0328\u032b\3\2\2\2\u0329\u0327\3\2\2\2\u0329")
        buf.write("\u032a\3\2\2\2\u032a\u032c\3\2\2\2\u032b\u0329\3\2\2\2")
        buf.write("\u032c\u032e\7$\2\2\u032d\u031b\3\2\2\2\u032d\u0324\3")
        buf.write("\2\2\2\u032e\u00e6\3\2\2\2\u032f\u0330\7)\2\2\u0330\u0331")
        buf.write("\7)\2\2\u0331\u0332\7)\2\2\u0332\u0336\3\2\2\2\u0333\u0335")
        buf.write("\5\u00e9u\2\u0334\u0333\3\2\2\2\u0335\u0338\3\2\2\2\u0336")
        buf.write("\u0337\3\2\2\2\u0336\u0334\3\2\2\2\u0337\u0339\3\2\2\2")
        buf.write("\u0338\u0336\3\2\2\2\u0339\u033a\7)\2\2\u033a\u033b\7")
        buf.write(")\2\2\u033b\u034a\7)\2\2\u033c\u033d\7$\2\2\u033d\u033e")
        buf.write("\7$\2\2\u033e\u033f\7$\2\2\u033f\u0343\3\2\2\2\u0340\u0342")
        buf.write("\5\u00e9u\2\u0341\u0340\3\2\2\2\u0342\u0345\3\2\2\2\u0343")
        buf.write("\u0344\3\2\2\2\u0343\u0341\3\2\2\2\u0344\u0346\3\2\2\2")
        buf.write("\u0345\u0343\3\2\2\2\u0346\u0347\7$\2\2\u0347\u0348\7")
        buf.write("$\2\2\u0348\u034a\7$\2\2\u0349\u032f\3\2\2\2\u0349\u033c")
        buf.write("\3\2\2\2\u034a\u00e8\3\2\2\2\u034b\u034e\5\u00efx\2\u034c")
        buf.write("\u034e\5\u00f1y\2\u034d\u034b\3\2\2\2\u034d\u034c\3\2")
        buf.write("\2\2\u034e\u00ea\3\2\2\2\u034f\u0351\t\23\2\2\u0350\u034f")
        buf.write("\3\2\2\2\u0351\u00ec\3\2\2\2\u0352\u0354\t\24\2\2\u0353")
        buf.write("\u0352\3\2\2\2\u0354\u00ee\3\2\2\2\u0355\u0357\t\25\2")
        buf.write("\2\u0356\u0355\3\2\2\2\u0357\u00f0\3\2\2\2\u0358\u0359")
        buf.write("\7^\2\2\u0359\u035a\t\26\2\2\u035a\u00f2\3\2\2\2\u035b")
        buf.write("\u035d\t\27\2\2\u035c\u035b\3\2\2\2\u035d\u035e\3\2\2")
        buf.write("\2\u035e\u035c\3\2\2\2\u035e\u035f\3\2\2\2\u035f\u00f4")
        buf.write("\3\2\2\2\u0360\u0364\7%\2\2\u0361\u0363\n\30\2\2\u0362")
        buf.write("\u0361\3\2\2\2\u0363\u0366\3\2\2\2\u0364\u0362\3\2\2\2")
        buf.write("\u0364\u0365\3\2\2\2\u0365\u00f6\3\2\2\2\u0366\u0364\3")
        buf.write("\2\2\2\u0367\u0369\7^\2\2\u0368\u036a\5\u00f3z\2\u0369")
        buf.write("\u0368\3\2\2\2\u0369\u036a\3\2\2\2\u036a\u0370\3\2\2\2")
        buf.write("\u036b\u036d\7\17\2\2\u036c\u036b\3\2\2\2\u036c\u036d")
        buf.write("\3\2\2\2\u036d\u036e\3\2\2\2\u036e\u0371\7\f\2\2\u036f")
        buf.write("\u0371\4\16\17\2\u0370\u036c\3\2\2\2\u0370\u036f\3\2\2")
        buf.write("\2\u0371\u00f8\3\2\2\2\u0372\u0374\t\31\2\2\u0373\u0372")
        buf.write("\3\2\2\2\u0374\u00fa\3\2\2\2\u0375\u0378\5\u00f9}\2\u0376")
        buf.write("\u0378\t\32\2\2\u0377\u0375\3\2\2\2\u0377\u0376\3\2\2")
        buf.write("\2\u0378\u00fc\3\2\2\2<\2\u0103\u0108\u010e\u01d1\u01d5")
        buf.write("\u01d8\u01da\u01e2\u01ea\u01ee\u01f5\u01f9\u01ff\u0205")
        buf.write("\u0207\u020e\u0215\u021c\u0220\u0224\u02ac\u02b5\u02b7")
        buf.write("\u02be\u02c0\u02c4\u02cd\u02da\u02e0\u02e4\u02ec\u02f9")
        buf.write("\u02ff\u0303\u030a\u0310\u0314\u0319\u031e\u0320\u0327")
        buf.write("\u0329\u032d\u0336\u0343\u0349\u034d\u0350\u0353\u0356")
        buf.write("\u035e\u0364\u0369\u036c\u0370\u0373\u0377\n\3)\2\3\66")
        buf.write("\3\3\67\4\3=\5\3>\6\3J\7\3K\b\b\2\2")
        return buf.getvalue()


class DrakeLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    STRING = 2
    NUMBER = 3
    INTEGER = 4
    DEF = 5
    RETURN = 6
    RAISE = 7
    FROM = 8
    IMPORT = 9
    AS = 10
    GLOBAL = 11
    NONLOCAL = 12
    ASSERT = 13
    IF = 14
    ELIF = 15
    ELSE = 16
    WHILE = 17
    FOR = 18
    IN = 19
    TRY = 20
    FINALLY = 21
    WITH = 22
    EXCEPT = 23
    LAMBDA = 24
    OR = 25
    AND = 26
    NOT = 27
    IS = 28
    NONE = 29
    TRUE = 30
    FALSE = 31
    CLASS = 32
    YIELD = 33
    DEL = 34
    PASS = 35
    CONTINUE = 36
    BREAK = 37
    ASYNC = 38
    AWAIT = 39
    NEWLINE = 40
    NAME = 41
    STRING_LITERAL = 42
    BYTES_LITERAL = 43
    DECIMAL_INTEGER = 44
    OCT_INTEGER = 45
    HEX_INTEGER = 46
    BIN_INTEGER = 47
    FLOAT_NUMBER = 48
    IMAG_NUMBER = 49
    DOT = 50
    ELLIPSIS = 51
    STAR = 52
    OPEN_PAREN = 53
    CLOSE_PAREN = 54
    COMMA = 55
    COLON = 56
    SEMI_COLON = 57
    POWER = 58
    ASSIGN = 59
    OPEN_BRACK = 60
    CLOSE_BRACK = 61
    OR_OP = 62
    XOR = 63
    AND_OP = 64
    LEFT_SHIFT = 65
    RIGHT_SHIFT = 66
    ADD = 67
    MINUS = 68
    DIV = 69
    MOD = 70
    IDIV = 71
    NOT_OP = 72
    OPEN_BRACE = 73
    CLOSE_BRACE = 74
    LESS_THAN = 75
    GREATER_THAN = 76
    EQUALS = 77
    GT_EQ = 78
    LT_EQ = 79
    NOT_EQ_1 = 80
    NOT_EQ_2 = 81
    AT = 82
    ARROW = 83
    ADD_ASSIGN = 84
    SUB_ASSIGN = 85
    MULT_ASSIGN = 86
    AT_ASSIGN = 87
    DIV_ASSIGN = 88
    MOD_ASSIGN = 89
    AND_ASSIGN = 90
    OR_ASSIGN = 91
    XOR_ASSIGN = 92
    LEFT_SHIFT_ASSIGN = 93
    RIGHT_SHIFT_ASSIGN = 94
    POWER_ASSIGN = 95
    IDIV_ASSIGN = 96
    SKIP_ = 97
    UNKNOWN_CHAR = 98

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'isa'", "'def'", "'return'", "'raise'", "'from'", "'import'", 
            "'as'", "'global'", "'nonlocal'", "'assert'", "'if'", "'elif'", 
            "'else'", "'while'", "'for'", "'in'", "'try'", "'finally'", 
            "'with'", "'except'", "'lambda'", "'or'", "'and'", "'not'", 
            "'is'", "'none'", "'true'", "'false'", "'class'", "'yield'", 
            "'del'", "'pass'", "'continue'", "'break'", "'async'", "'await'", 
            "'.'", "'...'", "'*'", "'('", "')'", "','", "':'", "';'", "'**'", 
            "'='", "'['", "']'", "'|'", "'^'", "'&'", "'<<'", "'>>'", "'+'", 
            "'-'", "'/'", "'%'", "'//'", "'~'", "'{'", "'}'", "'<'", "'>'", 
            "'=='", "'>='", "'<='", "'<>'", "'!='", "'@'", "'->'", "'+='", 
            "'-='", "'*='", "'@='", "'/='", "'%='", "'&='", "'|='", "'^='", 
            "'<<='", "'>>='", "'**='", "'//='" ]

    symbolicNames = [ "<INVALID>",
            "STRING", "NUMBER", "INTEGER", "DEF", "RETURN", "RAISE", "FROM", 
            "IMPORT", "AS", "GLOBAL", "NONLOCAL", "ASSERT", "IF", "ELIF", 
            "ELSE", "WHILE", "FOR", "IN", "TRY", "FINALLY", "WITH", "EXCEPT", 
            "LAMBDA", "OR", "AND", "NOT", "IS", "NONE", "TRUE", "FALSE", 
            "CLASS", "YIELD", "DEL", "PASS", "CONTINUE", "BREAK", "ASYNC", 
            "AWAIT", "NEWLINE", "NAME", "STRING_LITERAL", "BYTES_LITERAL", 
            "DECIMAL_INTEGER", "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", 
            "FLOAT_NUMBER", "IMAG_NUMBER", "DOT", "ELLIPSIS", "STAR", "OPEN_PAREN", 
            "CLOSE_PAREN", "COMMA", "COLON", "SEMI_COLON", "POWER", "ASSIGN", 
            "OPEN_BRACK", "CLOSE_BRACK", "OR_OP", "XOR", "AND_OP", "LEFT_SHIFT", 
            "RIGHT_SHIFT", "ADD", "MINUS", "DIV", "MOD", "IDIV", "NOT_OP", 
            "OPEN_BRACE", "CLOSE_BRACE", "LESS_THAN", "GREATER_THAN", "EQUALS", 
            "GT_EQ", "LT_EQ", "NOT_EQ_1", "NOT_EQ_2", "AT", "ARROW", "ADD_ASSIGN", 
            "SUB_ASSIGN", "MULT_ASSIGN", "AT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", 
            "AND_ASSIGN", "OR_ASSIGN", "XOR_ASSIGN", "LEFT_SHIFT_ASSIGN", 
            "RIGHT_SHIFT_ASSIGN", "POWER_ASSIGN", "IDIV_ASSIGN", "SKIP_", 
            "UNKNOWN_CHAR" ]

    ruleNames = [ "T__0", "STRING", "NUMBER", "INTEGER", "DEF", "RETURN", 
                  "RAISE", "FROM", "IMPORT", "AS", "GLOBAL", "NONLOCAL", 
                  "ASSERT", "IF", "ELIF", "ELSE", "WHILE", "FOR", "IN", 
                  "TRY", "FINALLY", "WITH", "EXCEPT", "LAMBDA", "OR", "AND", 
                  "NOT", "IS", "NONE", "TRUE", "FALSE", "CLASS", "YIELD", 
                  "DEL", "PASS", "CONTINUE", "BREAK", "ASYNC", "AWAIT", 
                  "NEWLINE", "NAME", "STRING_LITERAL", "BYTES_LITERAL", 
                  "DECIMAL_INTEGER", "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", 
                  "FLOAT_NUMBER", "IMAG_NUMBER", "DOT", "ELLIPSIS", "STAR", 
                  "OPEN_PAREN", "CLOSE_PAREN", "COMMA", "COLON", "SEMI_COLON", 
                  "POWER", "ASSIGN", "OPEN_BRACK", "CLOSE_BRACK", "OR_OP", 
                  "XOR", "AND_OP", "LEFT_SHIFT", "RIGHT_SHIFT", "ADD", "MINUS", 
                  "DIV", "MOD", "IDIV", "NOT_OP", "OPEN_BRACE", "CLOSE_BRACE", 
                  "LESS_THAN", "GREATER_THAN", "EQUALS", "GT_EQ", "LT_EQ", 
                  "NOT_EQ_1", "NOT_EQ_2", "AT", "ARROW", "ADD_ASSIGN", "SUB_ASSIGN", 
                  "MULT_ASSIGN", "AT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", 
                  "AND_ASSIGN", "OR_ASSIGN", "XOR_ASSIGN", "LEFT_SHIFT_ASSIGN", 
                  "RIGHT_SHIFT_ASSIGN", "POWER_ASSIGN", "IDIV_ASSIGN", "SKIP_", 
                  "UNKNOWN_CHAR", "SHORT_STRING", "LONG_STRING", "LONG_STRING_ITEM", 
                  "LONG_STRING_CHAR", "STRING_ESCAPE_SEQ", "NON_ZERO_DIGIT", 
                  "DIGIT", "OCT_DIGIT", "HEX_DIGIT", "BIN_DIGIT", "POINT_FLOAT", 
                  "EXPONENT_FLOAT", "INT_PART", "FRACTION", "EXPONENT", 
                  "SHORT_BYTES", "LONG_BYTES", "LONG_BYTES_ITEM", "SHORT_BYTES_CHAR_NO_SINGLE_QUOTE", 
                  "SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE", "LONG_BYTES_CHAR", 
                  "BYTES_ESCAPE_SEQ", "SPACES", "COMMENT", "LINE_JOINING", 
                  "ID_START", "ID_CONTINUE" ]

    grammarFileName = "Drake.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    @property
    def tokens(self):
        try:
            return self._tokens
        except AttributeError:
            self._tokens = []
            return self._tokens

    @property
    def indents(self):
        try:
            return self._indents
        except AttributeError:
            self._indents = []
            return self._indents

    @property
    def opened(self):
        try:
            return self._opened
        except AttributeError:
            self._opened = 0
            return self._opened

    @opened.setter
    def opened(self, value):
        self._opened = value

    @property
    def lastToken(self):
        try:
            return self._lastToken
        except AttributeError:
            self._lastToken = None
            return self._lastToken

    @lastToken.setter
    def lastToken(self, value):
        self._lastToken = value

    def reset(self):
        super().reset()
        self.tokens = []
        self.indents = []
        self.opened = 0
        self.lastToken = None

    def emitToken(self, t):
        super().emitToken(t)
        self.tokens.append(t)

    def nextToken(self):
        if self._input.LA(1) == Token.EOF and self.indents:
            for i in range(len(self.tokens)-1,-1,-1):
                if self.tokens[i].type == Token.EOF:
                    self.tokens.pop(i)

            self.emitToken(self.commonToken(LanguageParser.NEWLINE, '\n'))
            while self.indents:
                self.emitToken(self.createDedent())
                self.indents.pop()

            self.emitToken(self.commonToken(LanguageParser.EOF, "<EOF>"))
        next = super().nextToken()
        if next.channel == Token.DEFAULT_CHANNEL:
            self.lastToken = next
        return next if not self.tokens else self.tokens.pop(0)

    def createDedent(self):
        dedent = self.commonToken(LanguageParser.DEDENT, "")
        dedent.line = self.lastToken.line
        return dedent

    def commonToken(self, type, text, indent=0):
        stop = self.getCharIndex()-1-indent
        start = (stop - len(text) + 1) if text else stop
        return CommonToken(self._tokenFactorySourcePair, type, super().DEFAULT_TOKEN_CHANNEL, start, stop)

    @staticmethod
    def getIndentationCount(spaces):
        count = 0
        for ch in spaces:
            if ch == '\t':
                count += 8 - (count % 8)
            else:
                count += 1
        return count

    def atStartOfInput(self):
        return Lexer.column.fget(self) == 0 and Lexer.line.fget(self) == 1


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[39] = self.NEWLINE_action 
            actions[52] = self.OPEN_PAREN_action 
            actions[53] = self.CLOSE_PAREN_action 
            actions[59] = self.OPEN_BRACK_action 
            actions[60] = self.CLOSE_BRACK_action 
            actions[72] = self.OPEN_BRACE_action 
            actions[73] = self.CLOSE_BRACE_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))

    def NEWLINE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:

            tempt = Lexer.text.fget(self)
            newLine = re.sub("[^\r\n\f]+", "", tempt)
            spaces = re.sub("[\r\n\f]+", "", tempt)
            la_char = ""
            try:
                la = self._input.LA(1)
                la_char = chr(la)       # Python does not compare char to ints directly
            except ValueError:          # End of file
                pass

            # Strip newlines inside open clauses except if we are near EOF. We keep NEWLINEs near EOF to
            # satisfy the final newline needed by the single_put rule used by the REPL.
            try:
                nextnext_la = self._input.LA(2)
                nextnext_la_char = chr(nextnext_la)
            except ValueError:
                nextnext_eof = True
            else:
                nextnext_eof = False

            if self.opened > 0 or nextnext_eof is False and (la_char == '\r' or la_char == '\n' or la_char == '\f' or la_char == '#'):
                self.skip()
            else:
                indent = self.getIndentationCount(spaces)
                previous = self.indents[-1] if self.indents else 0
                self.emitToken(self.commonToken(self.NEWLINE, newLine, indent=indent))      # NEWLINE is actually the '\n' char
                if indent == previous:
                    self.skip()
                elif indent > previous:
                    self.indents.append(indent)
                    self.emitToken(self.commonToken(LanguageParser.INDENT, spaces))
                else:
                    while self.indents and self.indents[-1] > indent:
                        self.emitToken(self.createDedent())
                        self.indents.pop()
                
     

    def OPEN_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            self.opened += 1
     

    def CLOSE_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:
            self.opened -= 1
     

    def OPEN_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:
            self.opened += 1
     

    def CLOSE_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:
            self.opened -= 1
     

    def OPEN_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 5:
            self.opened += 1
     

    def CLOSE_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 6:
            self.opened -= 1
     

    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates is None:
            preds = dict()
            preds[39] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 0:
                return self.atStartOfInput()
         


