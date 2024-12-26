pub struct JahrRange {
    pub start_jahr: i32,
    pub ende_jahr: i32,
}

impl JahrRange {
    pub fn new(start_jahr: i32, ende_jahr: i32) -> JahrRange {
        JahrRange {
            start_jahr,
            ende_jahr,
        }
    }
}
