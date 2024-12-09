from unittest import TestCase

from pkg.rich_error import constant
from pkg.rich_error.error import RichError, error_code, error_meta, _error_info, get_error_info, _get_default_code


class RichErrorTest(TestCase):

    def test_error_one_layer(self):
        op = "tests.tests.RichErrorTest.test_error_one_layer"
        message = "layer one error occurred"

        err = RichError(operation=op).set_msg(message).set_code(40400)

        self.assertEqual(str(err), message)
        self.assertEqual(error_code(error=err), 40400)

    def test_error_one_layer_default_variable(self):
        op = "tests.tests.RichErrorTest.test_error_one_layer_default_variable"

        err = RichError(operation=op)

        self.assertEqual(str(err), "")
        self.assertEqual(error_code(error=err), 500_00)

    def test_error_two_layer_message_default(self):
        op = "tests.tests.RichErrorTest.test_error_two_layer_message_default"

        err1 = RichError(op)
        err2 = RichError(op).set_error(err1).set_meta({"user_id": 1})

        self.assertEqual(str(err2), "")
        self.assertEqual(error_code(error=err2), constant.DEFAULT_CODE)
        self.assertEqual(error_meta(err2), {"user_id": 1})

    def test_error_two_layer_message_in_layer_one(self):
        op = "tests.tests.RichErrorTest.test_error_two_layer_message_default"

        err1 = RichError(op).set_msg("an error").set_meta({"user_id": 1})
        err2 = RichError(op).set_error(err1)

        self.assertEqual(str(err2), "an error")
        self.assertEqual(error_code(err2), 50000)
        self.assertEqual(error_meta(err2), {"user_id": 1})

    def test_error_two_layer_message_custom_in_layer_two(self):
        op = "tests.tests.RichErrorTest.test_error_two_layer_message_custom_in_layer_one"

        err1 = RichError(op)
        err2 = RichError(op).set_error(err1).set_msg("an error")

        self.assertEqual(str(err2), "an error")
        self.assertEqual(error_code(err2), 50000)

    def test_error_three_layer_message_in_layer_one_layer_one_is_exception(self):
        op = "tests.tests.RichErrorTest.test_error_three_layer_message_in_layer_one_layer_one_is_exception"

        err1 = Exception("an error in exception")
        err2 = RichError(op).set_error(err1)
        err3 = RichError(op).set_error(err2)

        self.assertEqual(str(err3), "an error in exception")
        self.assertEqual(error_code(err3), 50000)
        self.assertEqual(error_meta(err3), {})

    def test_error_code_with_exception(self):
        err = Exception()

        self.assertEqual(error_code(err), 50000)

    def test_error_info_with_exception_error(self):
        err = Exception("hello")
        info = _error_info(err)

        self.assertEqual(info[constant.OPERATION], "")
        self.assertEqual(info[constant.CODE], constant.DEFAULT_CODE)
        self.assertEqual(info[constant.MESSAGE], "hello")
        self.assertEqual(info[constant.META], {})

    def test_error_info_with_rich_error_default_value(self):
        op = "tests.tests.RichErrorTest.test_error_info_with_rich_error"
        err = RichError(op)
        info = _error_info(err)

        self.assertEqual(info[constant.OPERATION], "tests.tests.RichErrorTest.test_error_info_with_rich_error")
        self.assertEqual(info[constant.CODE], constant.DEFAULT_CODE)
        self.assertEqual(info[constant.MESSAGE], "")
        self.assertEqual(info[constant.META], {})

    def test_error_info_with_rich_error_value(self):
        op = "tests.tests.RichErrorTest.test_error_info_with_rich_error"
        err = (RichError(op).set_code(40400).set_error(Exception("exception error")).set_meta({"user_id": 1}).
               set_msg("hello from test with rich error"))
        info = _error_info(err)

        self.assertEqual(info[constant.OPERATION], "tests.tests.RichErrorTest.test_error_info_with_rich_error")
        self.assertEqual(info[constant.CODE], 404_00)
        self.assertEqual(info[constant.MESSAGE], "hello from test with rich error")
        self.assertEqual(info[constant.META], {"user_id": 1})

    def test_error_three_layer_is_have_value(self):
        op = "tests.tests.RichErrorTest.test_error_three_layer_is_have_value"

        err1 = RichError(op).set_msg("error 1").set_code(40400).set_meta({"user_id": 1})
        err2 = RichError(op).set_error(err1).set_msg("error 2").set_code(42900).set_meta({"fullname": "alireza"})
        err3 = (RichError(op).set_error(err2).set_msg("error 3").set_code(50000).
                set_meta({"user_id": 1, "last_update": "2024"}))

        self.assertEqual(str(err3), "error 3")
        self.assertEqual(error_code(err3), 42900)

    def test_get_error_info_one_layer_exception(self):
        err = Exception("error")
        self.assertEqual(get_error_info(err), [
            {
                constant.OPERATION: "",
                constant.CODE: _get_default_code(),
                constant.MESSAGE: "error",
                constant.META: {},
            }
        ])

    def test_get_error_info_two_layer_layer_one_exception(self):
        op = "tests.tests.RichErrorTest.test_get_error_info_two_layer_layer_one_exception"

        err1 = Exception()
        err2 = RichError(op).set_error(err1)

        self.assertEqual(get_error_info(err2), [
            {
                constant.OPERATION: op,
                constant.CODE: _get_default_code(),
                constant.MESSAGE: "",
                constant.META: {},
            },
            {
                constant.OPERATION: "",
                constant.CODE: _get_default_code(),
                constant.MESSAGE: "",
                constant.META: {},
            },
        ])

    def test_get_error_info_two_layer_layer_one_exception2(self):
        op = "tests.tests.RichErrorTest.test_get_error_info_two_layer_layer_one_exception"

        err1 = Exception("error1")
        err2 = RichError(op).set_error(err1).set_meta({"user_id": 1}).set_code(40400).set_msg("error2")

        self.assertEqual(get_error_info(err2), [
            {
                constant.OPERATION: op,
                constant.CODE: 40400,
                constant.MESSAGE: "error2",
                constant.META: {"user_id": 1},
            },
            {
                constant.OPERATION: "",
                constant.CODE: _get_default_code(),
                constant.MESSAGE: "error1",
                constant.META: {},
            },
        ])

    def test_get_error_info_two_layer_rich_error(self):
        op = "tests.tests.RichErrorTest.test_get_error_info_two_layer_layer_one_exception"

        err1 = RichError(op).set_msg("error1").set_code(40400)
        err2 = RichError(op).set_error(err1).set_meta({"user_id": 1})

        self.assertEqual(get_error_info(err2), [
            {
                constant.OPERATION: op,
                constant.CODE: 40400,
                constant.MESSAGE: "error1",
                constant.META: {"user_id": 1},
            },
            {
                constant.OPERATION: op,
                constant.CODE: 40400,
                constant.MESSAGE: "error1",
                constant.META: {},
            },
        ])

    def test_get_error_info_three_layer_rich_error(self):
        op = "tests.tests.RichErrorTest.test_get_error_info_two_layer_layer_one_exception"

        err1 = RichError(op).set_msg("error1")
        err2 = RichError(op).set_error(err1).set_meta({"user_id": 1}).set_code(40300).set_msg("error2")
        err3 = RichError(op).set_error(err2).set_meta({"user_id": 1})

        self.assertEqual(get_error_info(err3), [
            {
                constant.OPERATION: op,
                constant.CODE: 40300,
                constant.MESSAGE: "error2",
                constant.META: {"user_id": 1},
            },
            {
                constant.OPERATION: op,
                constant.CODE: 40300,
                constant.MESSAGE: "error2",
                constant.META: {"user_id": 1},
            },
            {
                constant.OPERATION: op,
                constant.CODE: _get_default_code(),
                constant.MESSAGE: "error1",
                constant.META: {},
            },
        ])
